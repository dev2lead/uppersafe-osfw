#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import subprocess, tempfile

CLASSIC_MODE = "CLASSIC"
FORWARD_MODE = "FORWARD"

DEFAULT_IPBL = "IPBL"
DEFAULT_DNBL = "DNBL"
DEFAULT_DROP = "LOGDROP"

CONFIG_RULE_1 = "-F {}"
CONFIG_RULE_2 = "-A {} --match limit --limit 1/s --jump LOG"
CONFIG_RULE_3 = "-A {} --jump DROP"

APPEND_RULE_1 = "-A {} {} --protocol tcp --tcp-flags SYN SYN --jump {}"
APPEND_RULE_2 = "-A {} {} --protocol tcp --tcp-flags PSH PSH --jump {}"
APPEND_RULE_3 = "-A {} {} --protocol udp --match state --state NEW --jump {}"
APPEND_RULE_4 = "-A {} --source {} --jump {}"
APPEND_RULE_5 = "-A {} --destination {} --jump {}"
APPEND_RULE_6 = "-A {} --match string --string {} --algo bm --jump {}"

DELETE_RULE_1 = "-D {} {} --protocol tcp --tcp-flags SYN SYN --jump {}"
DELETE_RULE_2 = "-D {} {} --protocol tcp --tcp-flags PSH PSH --jump {}"
DELETE_RULE_3 = "-D {} {} --protocol udp --match state --state NEW --jump {}"
DELETE_RULE_4 = "-D {} --source {} --jump {}"
DELETE_RULE_5 = "-D {} --destination {} --jump {}"
DELETE_RULE_6 = "-D {} --match string --string {} --algo bm --jump {}"

class iptables:
    def __init__(self, network, mode, ipbl=DEFAULT_IPBL, dnbl=DEFAULT_DNBL, drop=DEFAULT_DROP):
        self.eth = network.get("eth")
        self.ppp = network.get("ppp")
        self.tun = network.get("tun")
        self.mode = mode.upper()
        self.ipbl = ipbl.upper()
        self.dnbl = dnbl.upper()
        self.drop = drop.upper()
        self.buffer = []

    def init(self):
        if self.mode:
            self.buffer.append(str(":{} - [0:0]").format(self.ipbl))
            self.buffer.append(str(":{} - [0:0]").format(self.dnbl))
            self.buffer.append(str(":{} - [0:0]").format(self.drop))
            self.buffer.append(CONFIG_RULE_1.format(self.ipbl))
            self.buffer.append(CONFIG_RULE_1.format(self.dnbl))
            self.buffer.append(CONFIG_RULE_1.format(self.drop))
            self.buffer.append(CONFIG_RULE_2.format(self.drop))
            self.buffer.append(CONFIG_RULE_3.format(self.drop))
            self.commit()
        if self.mode == CLASSIC_MODE:
            self.buffer.append(DELETE_RULE_1.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_1.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_2.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_2.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_3.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_3.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.commit()
            self.buffer.append(APPEND_RULE_1.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_1.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_2.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_2.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_3.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_3.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.commit()
        if self.mode == FORWARD_MODE:
            self.buffer.append(DELETE_RULE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(DELETE_RULE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.commit()
            self.buffer.append(APPEND_RULE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(APPEND_RULE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.commit()
        return 0

    def append(self, content, chain, label):
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(APPEND_RULE_4.format(chain, content, label))
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(APPEND_RULE_5.format(chain, content, label))
        if chain == self.dnbl:
            self.buffer.append(APPEND_RULE_6.format(chain, content[-128:], label))
        return 0

    def delete(self, content, chain, label):
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DELETE_RULE_4.format(chain, content, label))
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DELETE_RULE_5.format(chain, content, label))
        if chain == self.dnbl:
            self.buffer.append(DELETE_RULE_6.format(chain, content[-128:], label))
        return 0

    def commit(self):
        with tempfile.NamedTemporaryFile("w+") as fd:
            self.buffer = ["*filter"] + self.buffer + ["COMMIT"]
            for element in self.buffer:
                fd.write(element + "\n")
            fd.seek(0)
            self.buffer.clear()
            try:
                subprocess.check_output(["iptables-restore", "-n"], stdin=fd, stderr=subprocess.STDOUT)
            except Exception as error:
                return error
        return 0
