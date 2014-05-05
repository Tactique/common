import os

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker


class Engine:
    def __init__(self):
        db_file = 'sqlite:////%s' % os.path.join(os.environ['ROOTIQUE'], 'common', 'database', 'db.sqlite3')
        self.engine = sqla.create_engine(db_file, echo=False)
        my_sessionmaker = sessionmaker()
        my_sessionmaker.configure(bind=self.engine)

        self.my_sessionmaker = my_sessionmaker

    def get_session(self):
        return self.my_sessionmaker()

    def get_engine(self):
        return self.engine


engine = Engine()

if __name__ == '__main__':
    session = engine.get_session()
