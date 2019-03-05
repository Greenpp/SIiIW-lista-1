from entity import Node, Item, Entity


class Engine:
    """
    Genetic algorithm engine

    problem_name - Name of the problem
    knapsack_data_type - Data type
    nodes_num - Number of nodes
    items_num - Number of items
    max_capacity - Maximum capacity of knapsack
    min_speed - Minimal speed
    max_speed - Maximal speed
    renting_ratio - Not used
    edge_weight_type - Type of edges
    nodes - List of nodes
    population_size - Size of the population
    population - List of entities

    DATA_DIR - path to data directory
    """
    DATA_DIR = 'data/'

    def __init__(self, population_size, knapsack_method='greedy'):
        """
        :param population_size: int
            Number of entities in population
        :param knapsack_method: str, optional
            Method of item selection
                greedy - greedy algorithm, same items for all entities
                genetic - items are encoded into entity genome and optimized alongside with path
        """
        self.problem_name = None
        self.knapsack_data_type = None
        self.nodes_num = None
        self.items_num = None
        self.max_capacity = None
        self.min_speed = None
        self.max_speed = None
        self.renting_ratio = None
        self.edge_weight_type = None
        self.nodes = []

        self.knapsack_method = knapsack_method
        if knapsack_method == 'greedy':
            self.items = []
        elif knapsack_method == 'genetic':
            self.items = None
        else:
            print('Knapsack method error')
            exit(1)

        self.population_size = population_size
        self.population = []

    def init(self):
        """
        Initializes population with random entities
        """
        self.population = [Entity(self.nodes_num) for i in range(self.population_size)]

    def greedy_item_select(self, method='ratio'):
        """
        Marks items to steal with greedy algorithm

        :param method: str, optional
            Criteria by which items are picked
                weight - light first
                value - the most valuable first
                ratio - best value/weight ratio first
        """
        if method == 'weight':
            self.items.sort(key=lambda x: x.weight)
        elif method == 'value':
            self.items.sort(key=lambda x: x.value, reverse=True)
        elif method == 'ratio':
            self.items.sort(key=lambda x: x.ratio, reverse=True)
        else:
            print('Greedy method error')
            exit(1)

        weight_left = self.max_capacity
        for item in self.items:
            if item.weight <= weight_left:
                item.to_steal = True
                weight_left -= item.weight
                if weight_left == 0:
                    break

    def load_data(self, file_name):
        """
        Loads data from given file

        :param file_name: str
            Name of data file
        """
        data_path = Engine.DATA_DIR + file_name
        with open(data_path) as f:
            lines = list(f)

        self.problem_name = lines[0].split(':')[1].replace('\t', '').replace('\n', '')
        self.knapsack_data_type = lines[1].split(':')[1].replace('\t', '').replace('\n', '')
        self.nodes_num = int(lines[2].split(':')[1].replace('\t', '').replace('\n', ''))
        self.items_num = int(lines[3].split(':')[1].replace('\t', '').replace('\n', ''))
        self.max_capacity = int(lines[4].split(':')[1].replace('\t', '').replace('\n', ''))
        self.min_speed = float(lines[5].split(':')[1].replace('\t', '').replace('\n', ''))
        self.max_speed = float(lines[6].split(':')[1].replace('\t', '').replace('\n', ''))
        self.renting_ratio = float(lines[7].split(':')[1].replace('\t', '').replace('\n', ''))
        self.edge_weight_type = lines[8].split(':')[1].replace('\t', '').replace('\n', '')

        node_lines = lines[10:self.nodes_num + 10]
        item_lines = lines[self.nodes_num + 11:self.nodes_num + self.items_num + 11]

        for node_line in node_lines:
            _, x, y = node_line.split()

            node = Node(x, y)
            self.nodes.append(node)

        for item_line in item_lines:
            _, profit, weight, node = item_line.split()

            item = Item(int(profit), int(weight))

            if self.items is not None:
                self.items.append(item)

            node_id = int(node) - 1
            self.nodes[node_id].add_item(item)
