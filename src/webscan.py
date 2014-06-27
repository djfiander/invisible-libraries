#!/usr/bin/env python

import sys

import bottle
from bottle import route, template

import xISBN, complete

def shutdown():
    sys.exit()

@route('/test')
def wtf():
    bottle.response.set_header('content-type', 'text/plain')
    return "\n".join(' '.join([k, str(v)]) for (k, v) in bottle.request.environ.items())

@bottle.get('/scan')
def initial_scan():
    return template("scan")

@bottle.post('/scan')
@bottle.get('/scan/<isbn>')
def scan(isbn=None):
    if not isbn:
        isbn = bottle.request.forms.get('isbn')

    if isbn == "quit":
        shutdown()
    sys.stderr.write("SCAN %s!\n" % isbn)
    try:
        full_rec = complete.complete({'ISBN': isbn, 'TITLE': None})
    except xISBN.BadISBN as error:
        return template("scan", error="Bad ISBN: %s: %s" % (isbn, error))
    except:
        return template("scan", error="Error processing %s" % isbn)

    return template("scan", title= full_rec['TITLE'])

bottle.run(host='localhost', port=8080)
