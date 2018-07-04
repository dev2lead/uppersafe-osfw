#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import requests, string, re, ipaddress

class openphish:
    def __init__(self, log, range, agent, timeout):
        self.uri = ["https://www.openphish.com/feed.txt"]
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
        buffer = buffer.split(",")[0]
        for element in re.findall("^(https|http|ftps|ftp)(://)(.*)", buffer.strip()):
            buffer = str().join(element)
            buffer = buffer.split("#")[0]
            buffer = buffer.split("?")[0]
            buffer = buffer.split("/")[2]
            buffer = buffer.split(":")[0]
            if re.search("[.][a-z]+$", buffer.strip()):
                return [buffer.strip()]
        return []
