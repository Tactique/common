import os

import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker


class Engine:
	def __init__(self):
		db_file = 'sqlite:////%s' % os.path.join(os.environ['ROOTIQUE'], 'common', 'database', 'db.sqlite3')
		print(db_file)
		self.engine = sqla.create_engine(db_file, echo=False)

		self.my_sessionmaker = sessionmaker()
		self.my_sessionmaker.configure(bind=self.engine)

	def get_session(self):
		return self.my_sessionmaker()

	def get_engine(self):
		return self.engine


engine = Engine()
