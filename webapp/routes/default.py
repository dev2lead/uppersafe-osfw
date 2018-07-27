#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from .. import conf, db, app
from flask import g, session, request, abort, redirect, make_response, render_template
from datetime import datetime
import time, json

@app.before_request
def handler_before_request():
    g.db = db(conf.get("db"))

@app.teardown_request
def handler_teardown_request(e):
    g.pop("db")

@app.route("/", methods=["GET"])
def controller_root():
    return redirect("/app")
