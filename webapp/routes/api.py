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
    return make_response(json.dumps({"version": "1.0.0"}))

@app.route("/api/auth", methods=["POST"])
def controller_api_auth():
    return make_response(json.dumps({"message": "Not implemented yet"}))

@app.route("/api/events/<string:timeframe>", methods=["GET"])
def controller_api_events(timeframe):
    data = []
    utcnow = datetime.utcnow()
    period = {
        "5m": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 300,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 1
        ],
        "15m": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 900,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 1
        ],
        "60m": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 3600,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, utcnow.minute, 0).timestamp()) - 1
        ],
        "4h": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 14400,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 1
        ],
        "12h": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 43200,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 1
        ],
        "24h": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 86400,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, utcnow.hour, 0, 0).timestamp()) - 1
        ],
        "7d": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 604800,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 1
        ],
        "15d": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 1296000,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 1
        ],
        "30d": [
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 2592000,
            int(datetime(utcnow.year, utcnow.month, utcnow.day, 0, 0, 0).timestamp()) - 1
        ]
    }
    if timeframe in period:
        minimum, maximum = period[timeframe]
        query = g.db.session.query(g.db.models.events)
        query = query.order_by(g.db.models.events.id.desc())
        query = query.filter(g.db.models.events.creation >= minimum)
        query = query.filter(g.db.models.events.creation <= maximum)
        if "matchonly" in request.values and request.values.get("matchonly"):
            query = query.filter(g.db.models.events.port.in_(request.values.get("matchonly").split(",")))
        for row in query.yield_per(g.db.chunk):
            data.append({
                "source": row.source,
                "destination": row.destination,
                "port": row.port,
                "datetime": datetime.utcfromtimestamp(row.creation).strftime("%Y-%m-%d %H:%M:%S")})
    return make_response(json.dumps(data))
