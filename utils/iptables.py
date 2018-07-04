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

INI_CONFIG_1 = "-F {}"
INI_CONFIG_2 = "-A {} --match limit --limit 1/s --jump LOG"
INI_CONFIG_3 = "-A {} --source 217.78.11.148 --jump ACCEPT"
INI_CONFIG_4 = "-A {} --destination 217.78.11.148 --jump ACCEPT"
INI_CONFIG_5 = "-A {} --jump DROP"
INI_CONFIG_6 = "-A {} --source 217.78.11.148 --jump {}"
INI_CONFIG_7 = "-A {} --destination 217.78.11.148 --jump {}"

INI_APPEND_1 = "-A {} {} --protocol tcp --tcp-flags SYN SYN --jump {}"
INI_APPEND_2 = "-A {} {} --protocol tcp --tcp-flags PSH PSH --jump {}"
INI_APPEND_3 = "-A {} {} --protocol udp --match state --state NEW --jump {}"

INI_DELETE_1 = "-D {} {} --protocol tcp --tcp-flags SYN SYN --jump {}"
INI_DELETE_2 = "-D {} {} --protocol tcp --tcp-flags PSH PSH --jump {}"
INI_DELETE_3 = "-D {} {} --protocol udp --match state --state NEW --jump {}"

DYN_APPEND_1 = "-A {} --source {} --jump {}"
DYN_APPEND_2 = "-A {} --destination {} --jump {}"
DYN_APPEND_3 = "-A {} --match string --algo bm --string {} --jump {}"

DYN_DELETE_1 = "-D {} --source {} --jump {}"
DYN_DELETE_2 = "-D {} --destination {} --jump {}"
DYN_DELETE_3 = "-D {} --match string --algo bm --string {} --jump {}"

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
            self.buffer.append(INI_CONFIG_1.format(self.ipbl))
            self.buffer.append(INI_CONFIG_1.format(self.dnbl))
            self.buffer.append(INI_CONFIG_1.format(self.drop))
            self.buffer.append(INI_CONFIG_2.format(self.drop))
            self.buffer.append(INI_CONFIG_3.format(self.drop))
            self.buffer.append(INI_CONFIG_4.format(self.drop))
            self.buffer.append(INI_CONFIG_5.format(self.drop))
            self.buffer.append(INI_CONFIG_6.format(self.ipbl, self.dnbl))
            self.buffer.append(INI_CONFIG_6.format(self.dnbl, self.drop))
            self.buffer.append(INI_CONFIG_7.format(self.ipbl, self.dnbl))
            self.buffer.append(INI_CONFIG_7.format(self.dnbl, self.drop))
            self.commit()
        if self.mode == CLASSIC_MODE:
            self.buffer.append(INI_DELETE_1.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_1.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_2.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_2.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_3.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_3.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.commit()
            self.buffer.append(INI_APPEND_1.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_1.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_2.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_2.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_3.format("INPUT", str("--in-interface {}").format(self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_3.format("OUTPUT", str("--out-interface {}").format(self.eth), self.ipbl))
            self.commit()
        if self.mode == FORWARD_MODE:
            self.buffer.append(INI_DELETE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_DELETE_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.commit()
            self.buffer.append(INI_APPEND_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_1.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_2.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.ppp, self.eth), self.ipbl))
            self.buffer.append(INI_APPEND_3.format("FORWARD", str("--in-interface {} --out-interface {}").format(self.tun, self.eth), self.ipbl))
            self.commit()
        return 0

    def append(self, content, chain, label):
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DYN_APPEND_1.format(chain, content, label))
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DYN_APPEND_2.format(chain, content, label))
        if chain == self.dnbl:
            self.buffer.append(DYN_APPEND_3.format(chain, content[-128:], label))
        return 0

    def delete(self, content, chain, label):
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DYN_DELETE_1.format(chain, content, label))
        if chain == self.ipbl and ":" not in content:
            self.buffer.append(DYN_DELETE_2.format(chain, content, label))
        if chain == self.dnbl:
            self.buffer.append(DYN_DELETE_3.format(chain, content[-128:], label))
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
