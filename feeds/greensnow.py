#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import requests, string, re, ipaddress

class greensnow:
    def __init__(self, log, range, agent, timeout):
        self.uri = ["https://blocklist.greensnow.co/greensnow.txt"]
        self.log = log
        self.range = range
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": agent})
        self.timeout = timeout
        self.threats = set()

    def refresh(self):
        data = []
        for element in self.uri:
            try:
                response = self.session.get(element, timeout=self.timeout)
                if response.status_code == 200:
                    data = data + [x for x in response.text.splitlines() if x.strip()]
                    self.threats.clear()
            except:
                self.log.error(str("Request error in '{}' = '{}'").format(self.__class__.__name__, element))
        for element in data:
            for result in self.parse(element.lower()):
                if [x for x in string.whitespace + string.punctuation if x not in [".", ":", "/", "-", "_"] and x in result]:
                    self.log.warning(str("Parse error in '{}' = '{}'").format(self.__class__.__name__, result))
                else:
                    self.threats.add(result)
        return self.threats

    def parse(self, buffer):
        buffer = buffer.strip('"')
        buffer = buffer.strip("'")
        buffer = buffer.split("#")[0]
        if not self.range and re.search("[/][0-9]+$", buffer.strip()):
            return [str(x).strip() for x in ipaddress.ip_network(buffer.strip()).hosts()]
        if buffer.strip():
            return [buffer.strip()]
        return []
