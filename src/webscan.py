#!/usr/bin/env python

import sys

import bottle
from bottle import route, template

import xISBN, complete

debug = None

def shutdown():
    bottle.app().catchall = False
    sys.exit()

@route('/debug/<state>')
def set_debug(state):
    global debug

    debug = (state.lower() in ('on', 'yes', 'true'))
    return template("scan")

@route('/test')
def wtf():
    bottle.response.set_header('content-type', 'text/plain')
    return "\n".join(' '.join([k, str(v)]) for (k, v) in bottle.request.environ.items())

@route("/files/<filename:path>")
def send_file(filename):
    if (debug):
        sderr.write("Sending file %s\n" % filename)
    return bottle.static_file(filename, root="./files")

@bottle.get('/scan')
def initial_scan():
    return template("scan")

@bottle.post('/scan')
@bottle.get('/scan/<isbn>')
def scan(isbn=None):
    global debug

    if not isbn:
        isbn = bottle.request.forms.get('isbn')

    if isbn == "quit":
        shutdown()
    if debug:
        sys.stderr.write("SCAN %s!\n" % isbn)

    try:
        full_rec = complete.complete({'ISBN': isbn, 'TITLE': None})
    except xISBN.BadISBN as error:
        return template("scan", error="Bad ISBN: %s: %s" % (isbn, error))
    except:
        return template("scan", error="Error processing %s" % isbn)

    return template("scan", title= full_rec['TITLE'])

bottle.run(host='localhost', port=8080)
