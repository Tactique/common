import os

class BaseSeeder(object):
    def __init__(self, session):
        self.session = session
        try:
            database_path = os.path.join(os.environ['ROOTIQUE'], 'common', 'database')
            self.seed_data = os.path.join(database_path, 'seed_data')
            self.template_data = os.path.join(database_path, 'templates')
        except KeyError:
            raise Exception("Please define the $ROOTIQUE environment variable to your Tactique/ dir")


def print_delete_count(x):
    print("deleted %s" % x)
