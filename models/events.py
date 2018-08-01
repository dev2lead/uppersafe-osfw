#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

class events(declarative_base()):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    ts = Column(Integer, default=0)
    srcaddr = Column(String)
    dstaddr = Column(String)
    srcport = Column(Integer)
    dstport = Column(Integer)
    flag = Column(Integer, default=0)
