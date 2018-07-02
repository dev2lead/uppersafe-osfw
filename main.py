#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import sys, imp, hashlib, os

def main():
    if len(sys.argv) == 2 and "daemon/sensor" in sys.argv:
        daemon = imp.load_source("daemon", "daemon/sensor.py")
        daemon.sensor()
    if len(sys.argv) == 2 and "daemon/syncfw" in sys.argv:
        daemon = imp.load_source("daemon", "daemon/syncfw.py")
        daemon.syncfw()
    if len(sys.argv) == 2 and "webapp" in sys.argv:
        webapp = imp.load_source("webapp", "webapp/__init__.py")
        webapp.app.run(webapp.conf.get("host"), webapp.conf.get("port"))
    return 0

if __name__ == "__main__":
    main()
