#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import unittest

class test(unittest.TestCase):
    def test_default(self):
        self.assertEqual("TEST", "TEST")

if __name__ == "__main__":
    unittest.main()
