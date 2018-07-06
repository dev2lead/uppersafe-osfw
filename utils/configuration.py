#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import sys, os, yaml

class configuration(dict):
    def __init__(self):
        self.file = "config.default.yml"
        if os.path.isfile("config.yml"):
            self.file = "config.yml"
        try:
            self.reload()
        except Exception as error:
            print(error)
            sys.exit()

    def reload(self):
        with open(self.file, "r+") as fd:
            self.data = yaml.load(fd)
        self.verify({
            "db": str(),
            "host": str(),
            "port": int(),
            "mode": str(),
            "verbose": bool(),
            "threads": int(),
            "refreshDelay": int(),
            "queryTimeout": int(),
            "queryUserAgent": str(),
            "groupRange": bool(),
            "filterMode": str(),
            "streamFile": str(),
            "monitor": str(),
            "network": {
                "eth": str(),
                "ppp": str(),
                "tun": str()
                },
            "unbound": {
                "verbosity": int(),
                "hide-version": bool(),
                "interface": str(),
                "access-control": str()
                },
            "feeds": list(),
            "exemptions": list()
            }, self.data)
        self.update(self.data)
        return 0

    def verify(self, conf, data):
        for key, value in conf.items():
            if key not in data:
                raise Exception(str("Error in configuration = variable '{}' is not set").format(key))
            if type(data.get(key)) != type(value):
                raise Exception(str("Error in configuration = variable '{}' is not type '{}'").format(key, value.__class__.__name__))
            if isinstance(data.get(key), dict):
                self.verify(value, data.get(key))
        return 0
