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
        self.threats = {}

    def refresh(self):
        data = []
        for element in self.uri:
            try:
                response = self.session.get(element, timeout=self.timeout)
                if response.status_code == 200:
                    data = data + response.text.splitlines()
                    self.threats.clear()
            except:
                self.log.error(str("Request error in '{}' = '{}'").format(self.__class__.__name__, element))
        for element in data:
            try:
                content, revlookup = self.parse(element)
                if len([x for x in string.whitespace + string.punctuation if x not in [".", ":", "/", "-", "_"] and x in content]) != 0:
                    raise
                if len(content) != 0:
                    if not self.range and re.search("[/][0-9]+$", content):
                        self.threats.update([[str(x), []] for x in ipaddress.ip_network(content).hosts()])
                    else:
                        self.threats.update([[content, revlookup]])
            except:
                self.log.warning(str("Parse error in '{}' = '{}'").format(self.__class__.__name__, content))
        return self.threats

    def parse(self, content):
        content = str().join([x.lower() for x in content if x not in "\"\'"]).strip()
        try:
            revlookup = []
            content = content.split("#")[0]
            return content.strip(), revlookup
        except:
            pass
        return str(), []
