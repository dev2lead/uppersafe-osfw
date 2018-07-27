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
    source = Column(String)
    destination = Column(String)
    port = Column(Integer)
    creation = Column(Integer, default=0)
    modification = Column(Integer, default=0)
    flag = Column(Integer, default=0)
