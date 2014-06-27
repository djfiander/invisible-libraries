#
# load-data.py: load book data into the invisible libraries database
# 
# the input file is a CSV file containing the ISBN, author,
# title, and year of publication for each book. Any fields may be
# blank, and if the ISBN exists, then the other fields are
# ignored.

import sys, csv

import sqlite3
import xISBN
import z39query
from PyZ3950 import zmarc

verbose = False
inlines = 0
found = 0

def complete_rec(rec):
    # xISBN fieldname: CSV file fieldname
    move_corresponding = {'title': 'TITLE',
                          'author': 'AUTHOR',
                          'year': 'DATE',
                          'publisher': 'PUBLISHER'}

    # Fetch basic bib data from xISBN
    bibdata = xISBN.get_metadata(rec['ISBN'], move_corresponding.keys())

    for oclc_field, csv_field in move_corresponding.iteritems():
        if oclc_field not in bibdata:
            rec[csv_field] = ''
        else:
            # the CSV module can't handle unicode
            rec[csv_field] = bibdata[oclc_field].encode('utf_8')
    return(rec)

def check_holdings(conn, rec, rel_isbns):
    status = None
    if rec['ISBN']:
        res = conn.query('isbn=%(ISBN)s' % rec)
        if len(res) > 0:
            status = 'OWN'
        elif len(rel_isbns) > 0:
            for isbn in rel_isbns:
                res = conn.query('isbn=%s' % isbn)
                if len(res) > 0:
                    status = 'OWN RELATED'
                    break;
    else:
        pass

    return status

def find_or_add_author(db, author):
    with db:
        cur = db.cursor()
        cur.execute("SELECT id FROM authors WHERE au_name LIKE ?", (author,))
        r = cur.fetchone()
        if r is None:
            cur.execute("INSERT INTO authors (au_name) VALUES (?)", (author,))
            cur.execute("SELECT last_insert_rowid() AS id")
            r = cur.fetchone()

        cur.close()
        return r['id']
            
            
book_insert_stmt = """
INSERT INTO books (recorded_isbn, author, title,
                    publisher, pubdate, uwo_status)
SELECT ?, ?, ?, ?, ?, statuses.id FROM statuses WHERE status like ?
"""

def add_book(db, conn, rec):
    rel_isbns = set()
    with db:
        cur = db.cursor()
        if rec['ISBN']:
            cur.execute("INSERT INTO isbns (isbn) VALUES (?)", rec['ISBN'])
            rel_isbns = xISBN.xISBN(rec['ISBN']) 
            if (len(rel_isbns) > 0):
                cur.executemany("INSERT INTO isbns (isbn) VALUES (?)",
                                rel_isbns)
                cur.execute("INSERT INTO isbn_classes (master, isbn)
                             SELECT misbns.id, isbns.id
                             FROM isbns as misbns, isbns
                             WHERE misbns.isbn = ? AND isbns.isbn IN ?",
                            rec['ISBN'], rel_isbns)

        if rec['ISBN'] and not rec['TITLE']:
            rec = complete_rec(rec)

        if rec['AUTHOR']:
            au_id = find_or_add_author(rec['AUTHOR'])
        else:
            au_id = 'NULL'

        ownership = check_holdings(conn, rec, rel_isbns)
        cur.execute(book_insert_stmt, (isbn_id, au_id, rec['TITLE'],
                                       rec['PUBLISHER'], rec['DATE'],
                                       ownership['status']))

def increment_copy_count(db, isbn_id):
    with db:
        cur = db.cursor()
        cur.execute("UPDATE books SET numcopies = numcopies+1
                       WHERE recorded_isbn LIKE ?", (isbn_id,))
        cur.close()

def processtitle(db, conn, rec):
    pass

def processISBN(db, conn, rec):
    isbn = rec['ISBN']
    xISBN.validate(isbn)

    # query DB to see if this ISBN has already been
    # recorded if it has, then we don't need to find the
    # related ISBNs but we might need to check the
    # catalogue to see if we own this item

    cur = db.cursor()
    cur.execute('SELECT id FROM isbns WHERE isbn LIKE ?', (isbn,))
    r = cur.fetchone()
    if r is None:
        # The ISBN has not been recorded. Add it
        add_book(db, conn, rec)
    else:
        increment_copy_count(db, r['id'])
    cur.close()

def processFile(ifp, db, conn):
    global inlines, found
    icvs = csv.DictReader(ifp)

    for rec in icvs:
        inlines += 1

        if rec['ISBN'] != '':
            try:
                processISBN(db, conn, rec)
            except xISBN.BadISBN as ex:
                sys.stderr.write("Invalid ISBN for %s: '%s': %s\n" %
                                 (rec['Title'], isbn, ex.args[0]))
        else:
            processtitle(db, conn, rec)
                
def main():
    host = 'alpha.lib.uwo.ca'
    port = 210
    catname = 'INNOPAC'
    dbname = 'invisible'
    global verbose

    try:
        opts, args = getopt.getopt(ssys.argv[1:], "a:h:p:c:v")
    except getopt.GetoptError:
        sys.stderr.write("Usage: %s [-h host] [-p port] [-c catname] [-v] [-a affiliate-id\n" % sys.argv[0])
        sys.exit(2)

    for o, a in opts:
        if o == '-h':
            host = a
        elif o == '-p':
            port = int(a)
        elif o == '-c':
            catname = a
        elif o == '-v':
            verbose = True
        elif o = 'a':
            xISBN.register(a)

    conn = z39query.Z39query(host, port, catname, 'USMARC')
    if verbose:
        sys.stderr.write("Connected to %s, implementation ID = '%s'\n" %
                         (host, conn.targetImplementationId))

    db = sqlite3.connect('invisible.db')
    db.row_factory = sqlite3.Row

    if not args:
        processFile(sys.stdin, db, conn)
    else:
        for fname in args:
            with open(fname, 'r') as f:
                processFile(f, db, conn)
                

    if verbose:
        sys.stderr.write("Processed %d titles and found %d with %d connections\n" %
                         (inlines, found, conn.connects))
    conn.close()

if __name__ == "__main__":
    main()
