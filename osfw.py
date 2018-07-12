#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import sys, unittest, importlib
from tests import *

def main():
    if len(sys.argv) == 2 and "daemon/sensor" in sys.argv:
        daemon = importlib.import_module("daemon.sensor")
        daemon.sensor()
    if len(sys.argv) == 2 and "daemon/syncfw" in sys.argv:
        daemon = importlib.import_module("daemon.syncfw")
        daemon.syncfw()
    if len(sys.argv) == 2 and "webapp" in sys.argv:
        webapp = importlib.import_module("webapp")
        webapp.app.run(webapp.conf.get("host"), webapp.conf.get("port"))
    if len(sys.argv) == 2 and "assert" in sys.argv:
        unittest.main(argv=sys.argv[0:1])
    return 0

if __name__ == "__main__":
    main()
