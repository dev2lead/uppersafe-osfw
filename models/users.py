#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

class users(declarative_base()):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    ts = Column(Integer, default=0)
    hash = Column(String)
    fullname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    flag = Column(Integer, default=0)
