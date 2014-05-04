#!/usr/bin/env python

import sqlalchemy as sqla

import tables
from engine import engine

session = engine.get_session()
