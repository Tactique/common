#!/usr/bin/env python

from tables import game_engine, templates
from engine import engine


def main():
    print("Creating database with game related tables")
    sql_engine = engine.get_engine()
    game_engine.Base.metadata.create_all(sql_engine)
    templates.Base.metadata.create_all(sql_engine)


if __name__ == '__main__':
    main()
