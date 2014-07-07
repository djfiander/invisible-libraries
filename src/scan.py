#!/usr/bin/env python

import sys, getopt
import csv
import xISBN
import complete

outfile = None
ofp = sys.stdout
verbose = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "o:a:v")
except getopt.GetoptError:
    sys.stderr.write("Usage: %s [-o outfile] [-a affiliateID] [-v]\n" % sys.argv[0])
    sys.exit(2)

for o, a in opts:
    if o == '-o':
        ofp = open(a, "w")
    elif o == '-a':
        xISBN.register(a)
    elif o == '-v':
        verbose = True

ocsv = csv.DictWriter(ofp, ("ISBN","TITLE","AUTHOR","DATE","PUBLISHER"),
                                      lineterminator='\n')
ocsv.writeheader()

sys.stdout.write("? ")
for line in sys.stdin:
    isbn = line.strip()
    try:
        full_rec = complete.complete({'ISBN': isbn, 'TITLE': None})
    except xISBN.BadISBN as error:
        sys.stderr.write("Bad ISBN: %s: %s\n" % (isbn, error))
        next
    except:
        sys.stderr.write("Error processing %s\n" % isbn)
        raise

    if verbose:
        sys.stderr.write(full_rec['TITLE']+"\n\n")

    ocsv.writerow(full_rec)

    sys.stdout.write("? ")

ofp.close()
