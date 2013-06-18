#!/usr/bin/env python
#
# Take a csv file containing bibliographic data, and for every
# line that consists of just an ISBN, fetch bibliographic data
# for that ISBN and add it to the record

import sys, getopt

import csv
import xISBN

def processfile(ifp, ocsv):
    icsv = csv.DictReader(ifp)
    fields = ('title', 'author', 'year', 'publisher')
    for rec in icsv:
        if rec['ISBN'] and not rec['TITLE']:
            # Fetch basic bib data from xISBN
            try:
                bibdata = xISBN.get_metadata(rec['ISBN'], fields)
            except xISBN.BadISBN as error:
                print >>sys.stderr, "Bad ISBN: %s: %s" % (rec['ISBN'], error)
            except:
                print >>sys.stderr, "Error processing %s" % rec['ISBN']
                raise
            for f in fields:
                if f not in bibdata:
                    bibdata[f] = ''

            rec['TITLE'] = bibdata['title'].encode('latin_1')
            rec['AUTHOR'] = bibdata['author'].encode('latin_1')
            rec['DATE']  = bibdata['year']
            rec['PUBLISHER'] = bibdata['publisher'].encode('latin_1')

        ocsv.writerow(rec)

outfile = None
ofp = sys.stdout

try:
    opts, args = getopt.getopt(sys.argv[1:], "o:")
except getopt.GetoptError:
    sys.stderr.write("Usage: %s [-o outfile] [infile]\n" % sys.argv[0])
    sys.exit(2)

for o, a in opts:
    if o == '-o':
        ofp = open(a, "w")

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
