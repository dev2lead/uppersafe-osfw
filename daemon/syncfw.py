#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from daemon import conf, log, db, ipfw, dnfw
import time, importlib, re, json, socket, pebble

def ipbydn(data):
    result = set()
    try:
        for family, type, proto, name, (addr, port) in socket.getaddrinfo(data, 0):
            result.update([addr])
    except:
        pass
    return [x for x in result]

def dnbyip(data):
    result = set()
    try:
        for host, alias, addr in [socket.gethostbyaddr(data)]:
            result.update([host])
    except:
        pass
    return [x for x in result]

def resolv(data):
    if re.search("[.][a-z]+$", data):
        return ipbydn(data)
    else:
        return dnbyip(data)
    return []

class syncfw:
    def __init__(self):
        self.threats = {}
        self.feeds = {}
        self.start()

    def check_append(self, content, chain, label):
        if chain == ipfw.dnbl:
            error = dnfw.append(content)
        if chain != ipfw.drop:
            error = ipfw.append(content, chain, label)
        log.debug(str("[+] '{}' ({} -> {})").format(content, chain, label))
        return 0

    def check_delete(self, content, chain, label):
        if chain == ipfw.dnbl:
            error = dnfw.delete(content)
        if chain != ipfw.drop:
            error = ipfw.delete(content, chain, label)
        log.debug(str("[-] '{}' ({} -> {})").format(content, chain, label))
        return 0

    def fetch(self):
        for element in conf.get("feeds"):
            if element not in self.feeds.keys():
                module = getattr(importlib.import_module(str("feeds.{}").format(element)), element)
                self.feeds.update({element: module(log, conf.get("groupRange"), conf.get("queryUserAgent"), conf.get("queryTimeout"))})
        for element in sorted(self.feeds.keys()):
            if element not in conf.get("feeds"):
                self.feeds.pop(element)
        for element in self.feeds.values():
            self.threats.update([(x, []) for x in element.refresh()])
        log.info(str("[!] FETCH part 1/2 done ({} threats)").format(len(self.threats)))
        with pebble.ProcessPool(conf.get("threads")) as pool:
            instance = pool.map(resolv, sorted(self.threats.keys()), timeout=conf.get("queryTimeout"))
            iterator = instance.result()
            for index, element in enumerate(sorted(self.threats.keys()), start=1):
                try:
                    self.threats.update({element: next(iterator)})
                except:
                    self.threats.update({element: []})
                if index % round(len(self.threats) / 100) == 0 or index == len(self.threats):
                    log.info(str("{}% done... ({}/{})").format(int(100 / len(self.threats) * index), index, len(self.threats)))
            try:
                next(iterator)
                log.warning("Process pool is not empty (iterator object is still iterable)")
            except StopIteration:
                pass
        log.info(str("[!] FETCH part 2/2 done ({} threats)").format(len(self.threats)))
        return 0

    def clean(self):
        for element in conf.get("exemptions"):
            if re.search("[.][a-z]+$", element):
                db.session.add(db.models.exemptions(domain=element.lower()))
            else:
                db.session.add(db.models.exemptions(ipaddr=element.lower()))
        try:
            db.models.exemptions().metadata.drop_all(db.engine)
            db.models.exemptions().metadata.create_all(db.engine)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            log.error(error)
        log.info(str("[!] CLEAN part 1/2 done ({} threats)").format(len(self.threats)))
        for row in db.session.query(db.models.exemptions).order_by(db.models.exemptions.id).all():
            regex = []
            if row.domain:
                pattern = row.domain
            if row.ipaddr:
                pattern = row.ipaddr
            for index, node in enumerate(reversed(pattern.split("."))):
                if len(node) != 0 and index == 0 and node == "tld":
                    regex.append("((co|com|net|org|edu|gov)[.])?([a-z]+)")
                if len(node) != 0 and index == 0 and node != "tld":
                    regex.append(str("({})").format(node))
                if len(node) != 0 and index != 0:
                    regex.append(str("({})[.]").format(node))
                if len(node) == 0 and index != 0:
                    regex.append("((.*)[.])?")
            for element, revlookup in sorted(self.threats.items()):
                for record in revlookup:
                    if re.search(str("^{}$").format(str().join(reversed(regex))), record):
                        log.warning(str("Ignoring '{}' -> '{}' -> '{}'").format(element, record, str().join(reversed(regex))))
                        self.threats.pop(element)
                if element in self.threats:
                    if re.search(str("^{}$").format(str().join(reversed(regex))), element):
                        log.warning(str("Ignoring '{}' -> '{}'").format(element, str().join(reversed(regex))))
                        self.threats.pop(element)
        log.info(str("[!] CLEAN part 2/2 done ({} threats)").format(len(self.threats)))
        return 0

    def build(self):
        with open("assets/threats.txt", "w+") as fd:
            fd.write(str("\n").join(sorted(self.threats.keys())) + "\n")
        log.info(str("[!] BUILD part 1/1 done ({} threats)").format(len(self.threats)))
        return 0

    def merge(self):
        for row in db.session.query(db.models.threats).order_by(db.models.threats.id).all():
            if row.domain:
                if row.domain not in self.threats or json.loads(row.jsondata) != self.threats.get(row.domain):
                    for record in json.loads(row.jsondata):
                        self.check_delete(record, ipfw.ipbl, ipfw.dnbl)
                    self.check_delete(row.domain, ipfw.dnbl, ipfw.drop)
                    db.session.delete(row)
                else:
                    self.threats.pop(row.domain)
            if row.ipaddr:
                if row.ipaddr not in self.threats or json.loads(row.jsondata) != self.threats.get(row.ipaddr):
                    self.check_delete(row.ipaddr, ipfw.ipbl, ipfw.drop)
                    db.session.delete(row)
                else:
                    self.threats.pop(row.ipaddr)
        try:
            ipfw.commit()
            dnfw.commit()
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            log.error(error)
        log.info(str("[!] MERGE part 1/2 done ({} threats)").format(len(self.threats)))
        for element, revlookup in sorted(self.threats.items()):
            if re.search("[.][a-z]+$", element):
                for record in revlookup:
                    self.check_append(record, ipfw.ipbl, ipfw.dnbl)
                self.check_append(element, ipfw.dnbl, ipfw.drop)
                db.session.add(db.models.threats(domain=element, jsondata=json.dumps(revlookup)))
                self.threats.pop(element)
            else:
                self.check_append(element, ipfw.ipbl, ipfw.drop)
                db.session.add(db.models.threats(ipaddr=element, jsondata=json.dumps(revlookup)))
                self.threats.pop(element)
        try:
            ipfw.commit()
            dnfw.commit()
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            log.error(error)
        log.info(str("[!] MERGE part 2/2 done ({} threats)").format(len(self.threats)))
        return 0

    def reset(self):
        ipfw.init()
        dnfw.init()
        for row in db.session.query(db.models.threats).order_by(db.models.threats.id).all():
            if row.domain:
                if row.domain not in self.threats:
                    for record in json.loads(row.jsondata):
                        self.check_append(record, ipfw.ipbl, ipfw.dnbl)
                    self.check_append(row.domain, ipfw.dnbl, ipfw.drop)
            if row.ipaddr:
                if row.ipaddr not in self.threats:
                    self.check_append(row.ipaddr, ipfw.ipbl, ipfw.drop)
        try:
            ipfw.commit()
            dnfw.commit()
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            log.error(error)
        log.info(str("[!] RESET part 1/1 done ({} threats)").format(len(self.threats)))
        return 0

    def refresh(self, timestamp):
        if timestamp == 0 and conf.get("mode") in ["server", "standalone", "client"]:
            log.info(str("[!] Starting RESET..."))
            self.reset()
        if timestamp >= 0 and conf.get("mode") in ["server", "standalone", "client"]:
            log.info(str("[!] Starting FETCH..."))
            self.fetch()
        if timestamp >= 0 and conf.get("mode") in ["server", "standalone"]:
            log.info(str("[!] Starting CLEAN..."))
            self.clean()
        if timestamp >= 0 and conf.get("mode") in ["server"]:
            log.info(str("[!] Starting BUILD..."))
            self.build()
        if timestamp >= 0 and conf.get("mode") in ["server", "standalone", "client"]:
            log.info(str("[!] Starting MERGE..."))
            self.merge()
        return 0

    def start(self):
        timestamp = 0
        while timestamp >= 0:
            try:
                conf.reload()
            except Exception as error:
                log.critical(error)
                return 1
            if int(time.time()) - timestamp >= conf.get("refreshDelay"):
                self.refresh(timestamp)
                timestamp = int(time.time())
            else:
                time.sleep(60)
        return 0
