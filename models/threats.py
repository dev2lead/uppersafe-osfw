#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

class threats(declarative_base()):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True)
    ipaddr = Column(String, unique=True)
    jsondata = Column(String)
    creation = Column(Integer, default=0)
    modification = Column(Integer, default=0)
    flag = Column(Integer, default=0)
