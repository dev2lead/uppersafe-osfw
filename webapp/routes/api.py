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

@app.route("/api", methods=["GET"])
def controller_api_root():
    return make_response(json.dumps({"version": "1.0.0"}))

@app.route("/api/auth", methods=["POST"])
def controller_api_auth():
    return make_response(json.dumps({"message": "Not implemented yet"}))

@app.route("/api/events", methods=["GET"])
def controller_api_events():
    data = []
    period = {
        "5m": [int(time.time()) - 300, int(time.time())],
        "60m": [int(time.time()) - 3600, int(time.time())],
        "4h": [int(time.time()) - 14400, int(time.time())],
        "24h": [int(time.time()) - 86400, int(time.time())],
        "7d": [int(time.time()) - 604800, int(time.time())],
        "30d": [int(time.time()) - 2592000, int(time.time())]
    }
    if "range" in request.values and request.values.get("range") in period:
        minimum, maximum = period[request.values.get("range")]
        query = g.db.session.query(g.db.models.events)
        query = query.order_by(g.db.models.events.id.desc())
        query = query.filter(g.db.models.events.creation >= minimum)
        query = query.filter(g.db.models.events.creation <= maximum)
        if "only" in request.values and request.values.get("only"):
            query = query.filter(g.db.models.events.port.in_(request.values.get("only").split(",")))
        for row in query.yield_per(g.db.chunk):
            data.append({
                "source": row.source,
                "destination": row.destination,
                "port": row.port,
                "datetime": datetime.utcfromtimestamp(row.creation).strftime("%Y-%m-%d %H:%M:%S")})
    return make_response(json.dumps(data))
