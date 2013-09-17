#!/usr/bin/env python
#
# Take a csv file containing bibliographic data, and for every
# line that consists of just an ISBN, fetch bibliographic data
# for that ISBN and add it to the record

import sys, getopt

import csv
import xISBN

def complete(rec):
    # xISBN fieldname: CSV file fieldname
    move_corresponding = {'title': 'TITLE',
                          'author': 'AUTHOR',
                          'year': 'DATE',
                          'publisher': 'PUBLISHER'}

    if rec['ISBN'] and not rec['TITLE']:
        # Fetch basic bib data from xISBN
        bibdata = xISBN.get_metadata(rec['ISBN'], move_corresponding.keys())

        for oclc_field, csv_field in move_corresponding.iteritems():
            if oclc_field not in bibdata:
                rec[csv_field] = ''
            else:
                # the CSV module can't handle unicode
                rec[csv_field] = bibdata[oclc_field].encode('utf_8')
    return(rec)

def processfile(ifp, ocsv):
    for rec in csv.DictReader(ifp):
        try:
            rec = complete(rec)
        except xISBN.BadISBN as error:
            print >>sys.stderr, "Bad ISBN: %s: %s" % (rec['ISBN'], error)
            bibdata = dict()
        except:
            print >>sys.stderr, "Error processing %s" % rec['ISBN']
            raise
        ocsv.writerow(rec)

if __name__ == "__main__":
    outfile = None
    ofp = sys.stdout

    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:a:")
    except getopt.GetoptError:
        sys.stderr.write("Usage: %s [-o outfile] [-a affiliateID] [infile]\n" % sys.argv[0])
        sys.exit(2)

    for o, a in opts:
        if o == '-o':
            ofp = open(a, "w")
        elif o == '-a':
            xISBN.register(a)

    ocsv = csv.DictWriter(ofp, ("ISBN","TITLE","AUTHOR","DATE","PUBLISHER"),
                                      lineterminator='\n')
    ocsv.writeheader()

    if not args:
        processfile(sys.stdin, ocsv)
    else:
        for fname in args:
            with open(fname, "r") as ifp:
                processfile(ifp, ocsv)

    ofp.close()
