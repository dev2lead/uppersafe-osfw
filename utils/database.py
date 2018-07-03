#!/usr/bin/env python3
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##
# -*- coding: utf-8 -*-

import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class database:
    def __init__(self, file, verbose=False):
        self.engine = create_engine(str("sqlite:///{}").format(file), echo=verbose)
        self.models = importlib.import_module("models")
        self.models.exemptions().metadata.create_all(self.engine)
        self.models.threats().metadata.create_all(self.engine)
        self.models.events().metadata.create_all(self.engine)
        self.models.users().metadata.create_all(self.engine)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.session = self.session()
