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

@app.route("/api", methods=["GET"])
def controller_api_root():
    return make_response(json.dumps({"message": ""}))

@app.route("/api/auth", methods=["POST"])
def controller_api_auth():
    return make_response(json.dumps({"message": "Not implemented yet"}))

@app.route("/api/events", methods=["GET"])
def controller_api_events():
    data = []
    for row in g.db.session.query(g.db.models.events).order_by(g.db.models.events.id.desc()).yield_per(g.db.chunk).limit(100):
        data.append({
            "source": row.source,
            "destination": row.destination,
            "port": row.port,
            "datetime": datetime.utcfromtimestamp(row.creation).strftime("%Y-%m-%d %H:%M:%S")})
    return make_response(json.dumps(data))
