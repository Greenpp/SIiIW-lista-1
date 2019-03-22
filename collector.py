from os.path import isfile

import sqlalchemy as sql

from engine import Engine


class Collector:
    """
    Data collector
    """

    DATA_DIR = 'data/'

    def __init__(self, file_name, db_name='test_results'):
        """
        :param file_name: str
            Name of data file
        :param db_name: str, optional
            Name of database
        """
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
            test.assign_engine(self.engine)
            test.configure()
            if test.test_names():
                while test.run_next():
                    self.push_data_into_db()
                    self.engine.clear_logs()

    def add_test(self, test):
        """
        Adds new test for collector

        :param test: Test
            Test to add
        """
        self.tests.append(test)

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


class Test:
    """
    Configures engine parameters
    """

    def __init__(self, mutable_param, values, parameters=None):
        """

        :param mutable_param: str
            Name of parameter to test
        :param values: list
            List of values to test
        :param parameters: dict, optional
            Dictionary of immutable parameters values for this test
        """
        self.mutable_param = mutable_param
        self.values = list(values)
        self.parameters = parameters

        self.engine = None

    def assign_engine(self, engine):
        """
        Assigns engine to run tests on

        :param engine: Engine
            Engine to run tests on
        """
        self.engine = engine

    def configure(self):
        """
        Applies initial parameters to engine
        """
        if self.parameters is not None:
            for name, value in self.parameters.item():
                setattr(self.engine, name, value)

    def test_names(self):
        """
        Test if given parameters names are correct

        :return: bool
            If names are correct
        """
        if self.parameters is not None:
            for name in self.parameters.keys():
                if not hasattr(self.engine, name):
                    return False

        return hasattr(self.engine, self.mutable_param)

    def run_next(self):
        """
        Executes test for next value

        :return: bool
            True if test was executed
            False if there is no more values to test
        """
        if len(self.values) == 0:
            return False

        value = self.values.pop()
        setattr(self.engine, self.mutable_param, value)

        self.engine.run()

        return True
