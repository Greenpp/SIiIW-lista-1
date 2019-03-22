from engine import Engine
import sqlalchemy as sql
from os.path import isfile


class Collector:
    """
    Data collector
    """

    DATA_DIR = 'data/'

    def __init__(self, file_name, db_name='test_results'):
        self.db_name = db_name + '.db'
        self.data_file = file_name

        self.engine = Engine()
        self.connection = None

        self.tests = []

    def init(self):
        """
        Initializes database connection and loads data from given data file
        """
        self.engine.load_data(self.data_file)
        self.create_db()
        self.connect_to_db()

    def run(self):
        """
        Executes tests and saves results to db
        """
        for test in self.tests:
            # TODO execute test
            pass

    def create_db(self):
        """
        Creates db if doesnt exists
        """
        if not isfile(self.DATA_DIR + self.db_name):
            # TODO create db if doesnt exist
            pass

    def connect_to_db(self):
        """
        Connects to existing db
        """
        db_path = self.DATA_DIR + self.db_name

        self.connection = sql.create_engine('sqlite:///' + db_path).connect()

    def push_data_into_db(self):
        """
        Inserts current test logged data into database
        """
        # TODO push data into db
        pass
