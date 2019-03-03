from entity import Node, Item


class Engine:
    DATA_DIR = 'data/'

    def __init__(self):
        self.problem_name = None
        self.knapsack_data_type = None
        self.node_num = None
        self.item_num = None
        self.max_capacity = None
        self.min_speed = None
        self.max_speed = None
        self.renting_ratio = None
        self.edge_weight_type = None
        self.nodes = []

    def load_data(self, file_name):
        """
        Load data from given file

        :param file_name: str
            Name of data file
        """
        data_path = Engine.DATA_DIR + file_name
        with open(data_path) as f:
            lines = list(f)

        self.problem_name = lines[0].split(':')[1].replace('\t', '').replace('\n', '')
        self.knapsack_data_type = lines[1].split(':')[1].replace('\t', '').replace('\n', '')
        self.node_num = int(lines[2].split(':')[1].replace('\t', '').replace('\n', ''))
        self.item_num = int(lines[3].split(':')[1].replace('\t', '').replace('\n', ''))
        self.max_capacity = int(lines[4].split(':')[1].replace('\t', '').replace('\n', ''))
        self.min_speed = float(lines[5].split(':')[1].replace('\t', '').replace('\n', ''))
        self.max_speed = float(lines[6].split(':')[1].replace('\t', '').replace('\n', ''))
        self.renting_ratio = float(lines[7].split(':')[1].replace('\t', '').replace('\n', ''))
        self.edge_weight_type = lines[8].split(':')[1].replace('\t', '').replace('\n', '')

        node_lines = lines[10:self.node_num + 10]
        item_lines = lines[self.node_num + 11:self.node_num + self.item_num + 11]

        for node_line in node_lines:
            _, x, y = node_line.split()

            node = Node(x, y)
            self.nodes.append(node)

        for item_line in item_lines:
            _, profit, weight, node = item_line.split()

            item = Item(profit, weight)

            node_id = int(node) - 1
            self.nodes[node_id].add_item(item)
