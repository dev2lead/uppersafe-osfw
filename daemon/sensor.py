#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

from daemon import conf, log, db
import time, re, os, subprocess

class sensor:
    def __init__(self):
        self.ino = 0
        self.idx = 0
        self.start()

    def parse(self, content):
        try:
            iplist = subprocess.check_output(["hostname", "--all-ip"], stderr=subprocess.STDOUT).decode().strip().split(" ")
        except Exception as error:
            log.error(error)
            iplist = []
        for srcaddr, dstaddr, srcport, dstport in re.findall(".* SRC=([0-9a-f:.]+) DST=([0-9a-f:.]+) .* SPT=([0-9]+) DPT=([0-9]+) .*", content, re.IGNORECASE):
            if dstaddr in iplist:
                log.info(str("Blocking incoming '{}:{}' -> '{}:{}'").format(srcaddr, srcport, dstaddr, dstport))
                db.session_append(db.models.events(ts=int(time.time()), srcaddr=srcaddr, dstaddr=dstaddr, srcport=srcport, dstport=dstport, flag=1))
            if srcaddr in iplist:
                log.info(str("Blocking outgoing '{}:{}' -> '{}:{}'").format(srcaddr, srcport, dstaddr, dstport))
                db.session_append(db.models.events(ts=int(time.time()), srcaddr=srcaddr, dstaddr=dstaddr, srcport=srcport, dstport=dstport, flag=2))
        try:
            db.session_commit()
        except Exception as error:
            log.error(error)
        return 0

    def watch(self, file):
        self.idx = 0
        if not self.ino:
            self.idx = os.stat(file).st_size
        self.ino = os.stat(file).st_ino
        log.info(str("[!] Subscribing to file '{}'").format(file))
        with open(file) as fp:
            fp.seek(self.idx)
            try:
                while self.ino == os.stat(file).st_ino:
                    for element in [x for x in fp.read().splitlines() if x.strip()]:
                        self.parse(element)
                    time.sleep(1)
            except:
                pass
        log.warning(str("[!] Unsubscribing from file '{}' (probably because of log rotation)").format(file))
        return 0

    def start(self):
        while self.idx >= 0:
            try:
                conf.reload()
            except Exception as error:
                log.critical(error)
                return 1
            if os.path.exists(conf.get("monitor")):
                self.watch(conf.get("monitor"))
            else:
                log.error(str("[!] Could not find '{}' to monitor network events").format(conf.get("monitor")))
            time.sleep(1)
        return 0
