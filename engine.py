class Engine:
    DATA_DIR = 'data/'

    def __init__(self):
        problem_name = None
        knapsack_data_type = None
        node_num = None
        item_num = None
        max_capacity = None
        min_speed = None
        max_speed = None
        renting_ratio = None
        edge_weight_type = None
        nodes = None
        items = None

    def load_data(self, file_name):
        """
        Load data from given file

        :param file_name: str
            Name of data file
        """
        data_path = Engine.DATA_DIR + file_name
        with open(data_path) as f:
            pass
