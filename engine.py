import random

from matplotlib import pyplot as plt

from entity import Node, Item, Entity


class Engine:
    """
    Genetic algorithm engine

    problem_name - Name of the problem
    knapsack_data_type - Not used
    nodes_num - Number of nodes
    items_num - Number of items
    max_capacity - Maximum capacity of knapsack
    min_speed - Minimal speed
    max_speed - Maximal speed
    renting_ratio - Not used
    edge_weight_type - Not used
    nodes - List of nodes
    population - List of entities

    DATA_DIR - path to data directory
    """
    DATA_DIR = 'data/'

    def __init__(self, population_size=100, mutation_ratio=.01, keep_best=True, selection_method='roulette',
                 crossover_method='simple', mutation_method='swap', knapsack_method='greedy', **kwargs):
        """
        :param population_size: int, optional
            Number of entities in population
        :param mutation_ratio: float, optional
            Probability of mutation during crossover
        :param keep_best: bool, optional
            If the best entity should be passed to the next generation unchanged
        :param selection_method: str, optional
            Method of selection
                -roulette
                -tournament
        :param crossover_method: str, optional
            Method of crossover
                -simple
                -ox
                -cx
                -pmx
        :param mutation_method: str, option
            Method of mutation
                -swap
                -inverse
        :param knapsack_method: str, optional
            Method of item selection
                -greedy - greedy algorithm, same items for all entities
                -genetic - items are encoded into entity genome and optimized alongside with path TODO

        :param kwargs:
            :param tournament_size: int, optional
                Number of randomly picked entities for tournaments
            :param greedy_method: str, optional
                Criteria by which items are picked
                    -weight
                    -value
                    -ratio

        """
        self.population_size = population_size

        self.mutation_rate = mutation_ratio

        self.keep_best = keep_best

        self.selection_method = selection_method
        if selection_method == 'tournament':
            if 'tournament_size' not in kwargs:
                self.tournament_size = int(population_size * 8 / 100)
            else:
                self.tournament_size = kwargs['tournament_size']

        self.crossover_method = crossover_method

        self.mutation_method = mutation_method

        self.knapsack_method = knapsack_method
        if knapsack_method == 'greedy':
            if 'greedy_method' not in kwargs:
                self.greedy_method = 'ratio'
            else:
                self.greedy_method = kwargs['greedy_method']
            self.items = []
        elif knapsack_method == 'genetic':
            self.items = None
        else:
            print('Knapsack method error')
            exit(1)

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

        self.population = []

        self.logged_data = {'min': [],
                            'max': [],
                            'avg': []}

    def run(self, generations=None, fitness=None, info_every=None):
        """
        Runs algorithm for n generations or until given fitness is met and plots data at the end
        If neither generations or fitness is given it will run forever

        :param generations: int, optional
            Number of generations before algorithm will be terminated
        :param fitness: float, optional
            Minimal fitness at witch algorithm will be terminated
        :param info_every: int, optional
            At every n-th generation information about number and fitness will be printed
        """
        if self.knapsack_method == 'greedy':
            self.greedy_item_select()

        self.init()
        generation = 0
        while True:
            if info_every is not None and generation % info_every == 0:
                print('Generation: {}\nFitness: {}'.format(generation, self.population[0].fitness))
            if generations is not None and generation == generations:
                break
            if fitness is not None and self.population[0].fitness >= fitness:
                break
            self.next_generation()
            generation += 1

        self.plot_data()

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
        self.selection()
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

    def selection(self):
        """
        Creates new population
        """
        if self.selection_method == 'roulette':
            self.selection_roulette()
        elif self.selection_method == 'tournament':
            self.selection_tournament()
        else:
            print('Selection type error')
            exit(1)

    def selection_roulette(self):
        """
        Creates new population with weighted roulette system to pick parents
        """
        new_population = []

        if self.keep_best:
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

            child = p1.mate(p2, self.mutation_rate, self.crossover_method, self.mutation_method)
            new_population.append(child)

        self.population = new_population

    def selection_tournament(self):
        """
        Creates new population with random tournaments system to pick parents
        """
        new_population = []

        if self.keep_best:
            # passing best entity unchanged
            new_population.append(self.population[0])

        while len(new_population) < self.population_size:
            # select parents from 2 random tournaments
            p1 = max(random.sample(self.population, self.tournament_size), key=lambda x: x.fitness)
            p2 = max(random.sample(self.population, self.tournament_size), key=lambda x: x.fitness)

            child = p1.mate(p2, self.mutation_rate, self.crossover_method, self.mutation_method)
            new_population.append(child)

        self.population = new_population

    def greedy_item_select(self):
        """
        Marks items to steal with greedy algorithm

        Criteria by which items are picked
            weight - light first
            value - the most valuable first
            ratio - best value/weight ratio first
        """
        if self.greedy_method == 'weight':
            self.items.sort(key=lambda x: x.weight)
        elif self.greedy_method == 'value':
            self.items.sort(key=lambda x: x.value, reverse=True)
        elif self.greedy_method == 'ratio':
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
