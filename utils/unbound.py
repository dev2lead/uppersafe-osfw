#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import subprocess

class unbound:
    def __init__(self, conf):
        self.conf = conf
        self.file = "assets/unbound.conf"
        self.record = str("\t{}: '{} {} {}'").format("local-data", "{}", "A", "217.78.11.148").replace("'", '"')

    def init(self):
        with open(self.file, "w+") as fd:
            buffer = ["# Unbound configuration", "server:"]
            for key, value in self.conf.items():
                if isinstance(value, bool):
                    buffer.append(str("\t{}: {}").format(key, ["no", "yes"][int(value)]))
                else:
                    buffer.append(str("\t{}: {}").format(key, value))
            fd.write(str("\n").join(buffer) + "\n")
        return 0

    def append(self, content):
        with open(self.file, "r+") as fd:
            buffer = []
            for element in [x for x in fd.read().splitlines() if x.strip()]:
                if element != self.record.format(content):
                    buffer.append(element)
        with open(self.file, "w+") as fd:
            fd.write(str("\n").join(buffer) + "\n" + self.record.format(content) + "\n")
        return 0

    def delete(self, content):
        with open(self.file, "r+") as fd:
            buffer = []
            for element in [x for x in fd.read().splitlines() if x.strip()]:
                if element != self.record.format(content):
                    buffer.append(element)
        with open(self.file, "w+") as fd:
            fd.write(str("\n").join(buffer) + "\n")
        return 0

    def commit(self):
        try:
            subprocess.check_output(["unbound-control", "reload"], stderr=subprocess.STDOUT)
        except Exception as error:
            return error
        return 0
