import sqlalchemy as sql

from engine import Engine


class Collector:
    """
    Data collector
    """

    def __init__(self, file_name, db_name='genetic_data'):
        """
        :param file_name: str
            Name of data file
        :param db_name: str, optional
            Name of database
        """
        self.db_name = db_name
        self.data_file = file_name

        self.engine = Engine()
        self.connection = None

        self.tests = []

    def init(self):
        """
        Initializes database connection and loads data from given data file
        """
        self.engine.load_data(self.data_file)
        self.connect_to_db()

    def run(self):
        """
        Executes tests and saves results to db
        """
        test_num = len(self.tests)
        for i, test in enumerate(self.tests):
            print('Executing test {}/{}'.format(i + 1, test_num))
            test.assign_engine(self.engine)
            self.engine.reset_to_default()
            test.configure()
            test.push_exp_data(self.connection, self.data_file)
            if test.test_names():
                while test.run_next():
                    print('.', end='', flush=True)
                    test.push_test_data(self.connection)
                    self.engine.clear_logs()
                print('Done')
            else:
                print('Names error')

    def estimate_time(self):
        """
        Estimates time of collecting data

        :return: int
            Time in seconds
        """
        # time to compute default setting (100 generations of 100 entities)
        # time accurate for specific machine
        time_table = {'hard': 15,
                      'medium': 3,
                      'easy': 1.5,
                      'trivial': .7}

        difficulty = self.data_file.split('_')[0]
        time = 0
        for test in self.tests:
            test_pop_ratio = (100 if 'population' not in test.parameters else test.parameters['population']) / 100
            test_gen_ratio = (100 if 'generations' not in test.parameters else test.parameters['generations']) / 100
            time += time_table[difficulty] * len(test.values) * test_gen_ratio * test_pop_ratio

        return int(time)

    def close(self):
        """
        Closes db connection
        """
        if self.connection is not None:
            self.connection.close()

    def add_test(self, test):
        """
        Adds new test for collector

        :param test: Test
            Test to add
        """
        self.tests.append(test.copy())

    def connect_to_db(self):
        """
        Connects to existing db on mariadb local sever

        Requires manual server setup
        """
        self.connection = sql.create_engine('mysql+mysqldb://collector:1234@localhost:3306/' + self.db_name).connect()


class Test:
    """
    Configures engine parameters
    """

    def __init__(self, mutable_param, values, sample, parameters=None, desc=None):
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

        self.desc = desc
        if self.desc is None:
            self.desc = 'Test of {} with values:\n{}\nParams: {}'.format(mutable_param, self.values, parameters)
        self.desc = self.desc.replace('\'', '')

        self.values *= sample
        self.parameters = parameters

        self.engine = None
        self.exp_id = None

    def copy(self):
        """
        Creates a copy

        :return: Test
            Copy
        """
        cp = Test('', [], 0, None, '')

        cp.mutable_param = self.mutable_param
        cp.values = self.values.copy()
        cp.parameters = self.parameters
        cp.desc = self.desc

        return cp

    def push_exp_data(self, db_conn, file_name):
        """
        Inserts experiment data into db

        :param db_conn: Connection
            DB connection
        :param file_name: str
            Data file name
        """
        query = 'INSERT INTO `Experiments` (`desc`, file_name) VALUES (\'{}\', \'{}\')'.format(self.desc, file_name)
        result = db_conn.execute(query)

        self.exp_id = result.lastrowid

    def push_test_data(self, db_conn):
        """
        Inserts single tests data into db

        :param db_conn: Connection
            DB connection
        """
        pop_size = self.engine.population_size
        mut_rate = self.engine.mutation_rate
        keep_best = 1 if self.engine.keep_best else 0
        surv_rate = self.engine.survival_rate
        sel_meth = self.engine.selection_method
        cros_meth = self.engine.crossover_method
        mut_meth = self.engine.mutation_method
        greed_type = self.engine.greedy_type
        tour_size = self.engine.tournament_size if sel_meth == 'tournament' else -1
        gen_num = self.engine.generations
        f_num = len(self.engine.fitness_dict)

        param_query = 'INSERT INTO `Tests`' \
                      '(pop_size, mut_rate, keep_best, surv_rate, sel_meth, cros_meth, mut_meth, greed_type,' \
                      'tour_size, gen_num, f_num, id_EXP) VALUES' \
                      '({},{},{},{},\'{}\',\'{}\',\'{}\',\'{}\',{},{},{},{})'.format(pop_size, mut_rate, keep_best,
                                                                                     surv_rate, sel_meth,
                                                                                     cros_meth, mut_meth, greed_type,
                                                                                     tour_size,
                                                                                     gen_num, f_num,
                                                                                     self.exp_id)

        result = db_conn.execute(param_query)
        test_id = result.lastrowid

        data_query = 'INSERT INTO `Generations` (num, max_f, avg_f, min_f, id_TEST) ' \
                     'VALUES '

        data = self.engine.logged_data
        for num, (min_f, avg_f, max_f) in enumerate(zip(data['min'], data['avg'], data['max'])):
            if num > 0:
                data_query += ', '
            row = '({}, {}, {}, {}, {})'.format(num, max_f, avg_f, min_f, test_id)
            data_query += row

        db_conn.execute(data_query)

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
            for name, value in self.parameters.items():
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
