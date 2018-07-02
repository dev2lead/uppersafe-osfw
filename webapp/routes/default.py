#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from .. import conf, db, app
from flask import g, session, request, abort, redirect, make_response, render_template

@app.route("/", methods=["GET", "POST"])
def controller_root():
    return render_template("default.html")

'''
@app.route("/auth", methods=["GET", "POST"])

@app.route("/dashboard/stats", methods=["GET", "POST"])
|-> Graph
|-> Number of threats
|-> Number of attacks

@app.route("/dashboard/firewall", methods=["GET", "POST"])
|-> network
|-> monitor
|-> filterMode

@app.route("/dashboard/firewall/threats", methods=["GET", "POST"])
|-> groupRange
|-> refreshDelay
|-> queryTimeout
|-> queryUserAgent
|-> feeds
|-> exemptions

@app.route("/dashboard/firewall/rules", methods=["GET", "POST"])
|-> INPUT
|-> OUTPUT
|-> FORWARD
|-> IPBL
|-> DNBL
|-> LOGDROP

@app.route("/dashboard/dns", methods=["GET", "POST"])
|-> verbosity
|-> hide-version
|-> interface
|-> access-control
