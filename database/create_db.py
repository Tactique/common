#!/usr/bin/env python

from tables import Base
from engine import engine


def main():
    Base.metadata.create_all(engine.get_engine())


if __name__ == '__main__':
    main()
