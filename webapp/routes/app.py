#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from .. import conf, db, app
from flask import g, session, request, abort, redirect, make_response, render_template
from datetime import datetime
import json

@app.route("/app", methods=["GET"])
def controller_app_root():
    return render_template("default.html")

@app.route("/app/auth", methods=["GET", "POST"])
def controller_app_auth():
    return render_template("default.html")

@app.route("/app/dashboard", methods=["GET", "POST"])
def controller_app_dashboard():
    return render_template("default.html")
