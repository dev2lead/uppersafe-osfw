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
        try:
            self.models.exemptions().metadata.create_all(self.engine)
            self.models.threats().metadata.create_all(self.engine)
            self.models.events().metadata.create_all(self.engine)
            self.models.users().metadata.create_all(self.engine)
        except:
            pass
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.session = self.session()
        self.chunk = 100

    def session_append(self, row):
        try:
            self.session.add(row)
        except:
            raise
        return 0

    def session_delete(self, row):
        try:
            self.session.delete(row)
        except:
            raise
        return 0

    def session_commit(self):
        try:
            self.session.commit()
            self.session.expunge_all()
        except:
            self.session.rollback()
            raise
        return 0
