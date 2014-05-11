import os

class BaseSeeder(object):
    def __init__(self, session):
        self.session = session
        try:
            self.database_dir = os.path.join(os.environ['ROOTIQUE'], 'common', 'database')
        except KeyError:
            raise Exception("Please define the $ROOTIQUE environment variable to your Tactique/ dir")


def print_delete_count(x):
    print("deleted %s" % x)
