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

def processFile(ifp, conn, checkxISBN=False):
    global inlines, found
    icvs = csv.DictReader(ifp)

    for rec in icvs:
        inlines += 1

        if rec['ISBN'] != '':
            try:
                xISBN.validate(rec['ISBN'])
            except xISBN.BadISBN, ex:
                sys.stderr.write("Invalid ISBN for %s: '%s': %s\n" %
                                 (rec['Title'], rec['ISBN'], ex.args[0]))
                continue

            # query DB to see if this ISBN has already been
            # recorded if it has, then we don't need to find the
            # related ISBNs but we might need to check the
            # catalogue to see if we own this item

def main():
    host = 'alpha.lib.uwo.ca'
    port = 210
    catname = 'INNOPAC'
    dbname = 'invisible'
    checkxISBN = False
    global verbose

    try:
        opts, args = getopt.getopt(ssys.argv[1:], "h:p:c:vx")
    except getopt.GetoptError:
        sys.stderr.write("Usage: %s [-h host] [-p port] [-c catname] [-v] [-x]\n" % sys.argv[0])
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
        elif o == 'x':
            checkxISBN = True

    conn = z39query.Z39query(host, port, catname, 'USMARC')
    if verbose:
        sys.stderr.write("Connected to %s, implementation ID = '%s'\n" %
                         (host, conn.targetImplementationId))

    if not args:
        processFile(sys.stdin, conn, checkxISBN)
    else:
        for fname in args:
            with open(fname, 'r') as f:
                processFile(f, conn, checkxISBN)
                

    if verbose:
        sys.stderr.write("Processed %d titles and found %d with %d connections\n" %
                         (inlines, found, conn.connects))
    conn.close()
if __name__ == "__main__":
    main()
