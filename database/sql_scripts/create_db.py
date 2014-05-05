#!/usr/bin/env python

from tables.game_engine import Base
from engine import engine


def main():
    print("Creating database with game related tables")
    Base.metadata.create_all(engine.get_engine())


if __name__ == '__main__':
    main()
