#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import requests, re, ipaddress

class phishtank:
    def __init__(self, log, range, agent, timeout):
        self.uri = ["https://data.phishtank.com/data/online-valid.csv"]
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
                self.log.error(str("Request error in '{}' = {}").format(self.__class__.__name__, element))
        for element in data:
            try:
                result = self.parse(element.lower())
                self.threats.update(result)
            except:
                self.log.warning(str("Parse error in '{}' = {}").format(self.__class__.__name__, element))
        return self.threats

    def parse(self, buffer):
        buffer = buffer.strip('"')
        buffer = buffer.split(",")[1]
        for element in re.findall("^(https|http|ftps|ftp)(://)(.*)", buffer.strip()):
            buffer = str().join(element)
            buffer = buffer.split("#")[0]
            buffer = buffer.split("?")[0]
            buffer = buffer.split("/")[2]
            buffer = buffer.split(":")[0]
            if re.search("[.][a-z]+$", buffer.strip()):
                return [buffer.strip()]
        return []
