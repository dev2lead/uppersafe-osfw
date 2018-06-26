#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from utils import configuration, database
import flask, hashlib, os

conf = configuration()
db = database(conf.get("db"))
app = flask.Flask(__name__)
app.debug = conf.get("debug")
app.session_cookie_name = "session"
app.secret_key = hashlib.md5(os.urandom(24)).hexdigest()

import routes
