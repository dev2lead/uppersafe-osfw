#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import requests, string, re, ipaddress

class openphish:
    def __init__(self, log, group, agent, timeout):
        self.uri = ["https://www.openphish.com/feed.txt"]
        self.log = log
        self.group = group
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": agent})
        self.timeout = timeout

    def refresh(self):
        data = []
        threats = {}
        for element in self.uri:
            try:
                response = self.session.get(element, timeout=self.timeout)
                if response.status_code == 200:
                    data = data + response.text.splitlines()
            except:
                self.log.error(str("Request error in '{}' = '{}'").format(self.__class__.__name__, element))
        if len(data) == 0:
            with open(str("assets/cache/{}.txt").format(self.__class__.__name__), "r+") as fp:
                data = fp.read().splitlines()
        else:
            with open(str("assets/cache/{}.txt").format(self.__class__.__name__), "w+") as fp:
                fp.write(str("\n").join(data))
        for element in data:
            try:
                content, revlookup = self.parse(element)
                if len([x for x in string.whitespace + string.punctuation if x not in [".", ":", "/", "-", "_"] and x in content]) != 0:
                    raise
                if len(content) != 0:
                    if not self.group and re.search("[/][0-9]+$", content):
                        threats.update([[str(x), []] for x in ipaddress.ip_network(content).hosts()])
                    else:
                        threats.update([[content, revlookup]])
            except:
                self.log.warning(str("Parse error in '{}' = '{}'").format(self.__class__.__name__, content))
        return threats

    def parse(self, content):
        content = str().join([x.lower() for x in content if x not in "\"\'"]).strip()
        try:
            revlookup = []
            content = content.split(",")[0]
            if not re.search("^(https|http|ftps|ftp)(://)(.*)", content.strip()):
                raise
            content = content.split("#")[0]
            content = content.split("?")[0]
            content = content.split("/")[2]
            content = content.split(":")[0]
            if not re.search("[.][a-z]+$", content.strip()):
                raise
            return content.strip(), revlookup
        except:
            pass
        return str(), []
