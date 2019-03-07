from entity import Node, Item, Entity
import random
from matplotlib import pyplot as plt


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

        self.logged_data = {'min': [],
                            'max': [],
                            'avg': []}

    def init(self):
        """
        Initializes population with random entities
        """
        self.population = [Entity(self.nodes_num) for i in range(self.population_size)]
        self.test()
        self.sort()
        self.log_data()

    def test(self):
        """
        Calculates fitness for new entities in population
        """
        for entity in self.population:
            if entity.fitness is None:
                entity.test(self.nodes, self.min_speed, self.max_speed, self.max_capacity)

    def sort(self):
        """
        Sorts population base on fitness
        """
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def next_generation(self):
        """
        Procedes to next generation, selects new population, tests and sorts it
        """
        self.selection(method='tournament')
        self.test()
        self.sort()
        self.log_data()

    def log_data(self):
        """
        Stores current generation max, min and avg fitness
        """
        fitness_data = [e.fitness for e in self.population]

        min_fitness = min(fitness_data)
        max_fitness = max(fitness_data)
        avg_fitness = sum(fitness_data) / len(fitness_data)

        self.logged_data['min'].append(min_fitness)
        self.logged_data['max'].append(max_fitness)
        self.logged_data['avg'].append(avg_fitness)

    def plot_data(self):
        """
        Plots logged data
        """
        plt.plot(self.logged_data['min'], 'r')
        plt.plot(self.logged_data['avg'], 'y')
        plt.plot(self.logged_data['max'], 'g')

        plt.xlabel('Generation')
        plt.ylabel('Fitness')

        plt.title(self.problem_name)

        plt.show()

    def selection(self, method='roulette', **kwargs):
        """
        Creates new population with given method

        :param method: str, optional
            Name of the selection method
        :param keep_best: bool, optional
            If best entity should be passed unchanged
        """
        selection_methods = {'roulette': self.selection_roulette,
                             'tournament': self.selection_tournament}

        if method not in selection_methods:
            print('Selection type error')
            exit(1)

        selection_methods[method]()

    def selection_roulette(self, keep_best=True):
        """
        Creates new population with weighted roulette system to pick parents

        :param keep_best: bool, optional
            If best entity should be passed unchanged
        """
        new_population = []

        if keep_best:
            # passing best entity unchanged
            new_population.append(self.population[0])

        weights = [e.fitness for e in self.population]

        # shift to avoid negative values
        min_weight = min(weights)
        shifted_weights = [w - min_weight + 1 for w in weights]

        # normalization
        weight_sum = sum(shifted_weights)
        norm_weights = [w / weight_sum for w in shifted_weights]

        # mating
        while len(new_population) < self.population_size:
            p1, p2 = random.choices(self.population, weights=norm_weights, k=2)

            child = p1.mate(p2)
            new_population.append(child)

        self.population = new_population

    def selection_tournament(self, size=8, keep_best=True):
        """
        Creates new population with random tournaments system to pick parents

        :param size: int
            Number of randomly picked entities for tournament
        :param keep_best: If best entity should be passed unchanged
        """
        new_population = []

        if keep_best:
            # passing best entity unchanged
            new_population.append(self.population[0])

        while len(new_population) < self.population_size:
            # select parents from 2 random tournaments
            p1 = max(random.sample(self.population, size), key=lambda x: x.fitness)
            p2 = max(random.sample(self.population, size), key=lambda x: x.fitness)

            child = p1.mate(p2)
            new_population.append(child)

        self.population = new_population

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

            node = Node(float(x), float(y))
            self.nodes.append(node)

        for item_line in item_lines:
            _, profit, weight, node = item_line.split()

            item = Item(int(profit), int(weight))

            if self.items is not None:
                self.items.append(item)

            node_id = int(node) - 1
            self.nodes[node_id].add_item(item)
