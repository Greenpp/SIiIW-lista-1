from random import random

import networkx as nx
from matplotlib import pyplot as plt

from genetics import Genotype


class Entity:
    """
    Entity representing single path

    genotype - Encoded path
    fitness - Score of this path
    """

    def __init__(self, nodes_num=None):
        """
        :param nodes_num: int, optional
            Total number of nodes
        """
        self.genotype = None if nodes_num is None else Genotype(nodes_num)
        self.fitness = None

    def copy(self):
        """
        Creates copy of entity

        :return: Entity
            Copy
        """
        cp = Entity()
        cp.genotype = self.genotype.copy()
        cp.fitness = self.fitness

        return cp

    def test(self, nodes, min_speed, max_speed, max_weight, fitness_dict, greedy_type='static', **kwargs):
        """
        Calculates fitness

        Used formula:
            g(y) - f(x, y)
        Where:
            g(y) - sum of stolen items
            f(x, y) - total time of travers

        :param nodes: list
            List of all nodes
        :param max_speed: float
            Speed with empty bag
        :param min_speed: float
            Speed with full bag
        :param max_weight: int
            Capacity of bag
        :param fitness_dict: dict
            Dictionary mapping genes sequence -> fitness value
        :param greedy_type: str, optional
            Type of greedy item marking
        :param kwargs:
            :param greedy_method: str, optional
                Criteria by which items are picked
                    -weight
                    -value
                    -ratio
        """
        self.fitness = 0

        fitness_key = self.genotype.create_key()
        if fitness_key in fitness_dict:
            # if already calculated read value
            self.fitness = fitness_dict[fitness_key]
            return

        weight = 0
        path = self.genotype.decode()

        if greedy_type == 'dynamic':
            if 'greedy_method' not in kwargs:
                print('Argument greedy_method required for dynamic greedy algorithm')
                exit(1)

            self.dynamic_greedy(path, nodes, max_weight, kwargs['greedy_method'])

        for id1, id2 in path:
            node1 = nodes[id1]
            node2 = nodes[id2]

            city_value, city_weight = node1.steal()

            weight += city_weight
            speed = max_speed - weight * (max_speed - min_speed) / max_weight
            time = node1.calculate_time_to(node2, speed)

            self.fitness += city_value
            self.fitness -= time

        # save new value
        fitness_dict[fitness_key] = self.fitness

    def dynamic_greedy(self, path, nodes, max_weight, greedy_method='ratio'):
        """
        Marks items base on current nodes order

        :param path: list
            Sequence of nodes for which items should be scaled
        :param nodes: list
            List of all nodes
        :param max_weight: int
            Capacity of bag
        :param greedy_method: str, optional
            Criteria by which items are marked
        """
        # build distance, items list
        distances = []
        total_distance = 0
        for id1, id2 in path:
            node1 = nodes[id1]
            node2 = nodes[id2]

            distance = node1.calculate_distance_to(node2)
            items = node1.items

            total_distance += distance

            distances.append([items, distance])

        # sum from finish to get total distance foe each item
        distances.reverse()
        for i in range(len(distances) - 1):
            distances[i + 1][1] += distances[i][1]

        # normalize for scaling and shift to avoid 0
        for pair in distances:
            pair[1] = 1 - (pair[1] / total_distance) + 1

        # create item, weighted value list
        scaled_items = []
        for pair in distances:
            for item in pair[0]:
                value = None
                if greedy_method == 'ratio':
                    value = item.ratio
                    value *= pair[1]
                elif greedy_method == 'weight':
                    value = item.weight
                    value *= (-2 - pair[1])
                elif greedy_method == 'value':
                    value = item.value
                    value *= pair[1]

                scaled_items.append((item, value))

        # sort
        if greedy_method == 'ratio':
            scaled_items.sort(key=lambda x: x[1], reverse=True)
        elif greedy_method == 'weight':
            scaled_items.sort(key=lambda x: x[1])
        elif greedy_method == 'value':
            scaled_items.sort(key=lambda x: x[1], reverse=True)

        # greedy mark items
        weight_left = max_weight
        for item, _ in scaled_items:
            if item.weight <= weight_left:
                item.to_steal = True
                weight_left -= item.weight
            else:
                item.to_steal = False

    def mate(self, entity, mutation_rate=.01, crossover_method='simple', mutation_method='swap'):
        """
        Creates child with second entity

        :param entity: Entity
            Parent 2
        :param mutation_rate: float, optional
            Probability of mutation
        :param crossover_method: str, optional
            Crossover method
        :param mutation_method: str, optional
            Mutation method
        :return: Entity
            Child
        """
        p1 = self.genotype
        p2 = entity.genotype

        # crossover
        child_genotype = p1.crossover(p2, method=crossover_method)

        # mutation
        rnd = random()
        if rnd < mutation_rate:
            child_genotype.mutate(method=mutation_method)

        child = Entity()
        child.genotype = child_genotype

        return child

    def visualize(self, nodes):
        """
        Draws encoded path as directed graph

        Robbed cities are in red, not in blue
        """
        edges = self.genotype.decode()

        # partition nodes
        robbed_cities = []
        skipped_cities = []
        first_city = self.genotype.nodes_order[0]
        for i in self.genotype.nodes_order[1:]:
            if nodes[i].steal() == (0, 0):
                skipped_cities.append(i)
            else:
                robbed_cities.append(i)

        g = nx.DiGraph(edges)
        layout = nx.circular_layout(g)

        # draw
        nx.draw_networkx_nodes(g, layout, nodelist=[first_city], node_color='y')
        nx.draw_networkx_nodes(g, layout, nodelist=robbed_cities, node_color='r')
        nx.draw_networkx_nodes(g, layout, nodelist=skipped_cities, node_color='b')
        nx.draw_networkx_edges(g, layout)

        # add labels
        labels = {n: n for n in self.genotype.nodes_order}
        nx.draw_networkx_labels(g, layout, labels)

        plt.axis('off')
        plt.show()


class Node:
    """
    Node representing city

    position - Coordinates of the city
    items - Items available in the city
    """

    def __init__(self, x, y):
        """
        :param x: float
            X coordinate of node
        :param y: float
            Y coordinate of node
        """
        self.position = (x, y)
        self.items = []
        self.sort_order = None

    def add_item(self, item):
        """
        Inserts new item to node

        :param item: Item
            New item
        """
        self.items.append(item)

    def calculate_distance_to(self, node):
        """
        Calculates distance to another node

        :param node: Node
            Other node
        :return: float
            Distance
        """
        x1, y1 = self.position
        x2, y2 = node.position

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

        return distance

    def calculate_time_to(self, node, speed):
        """
        Calculates time it takes to get from this node to another with given speed

        :param node: Node
            Other node
        :param speed: float
            Given speed
        :return: float
            Time
        """
        distance = self.calculate_distance_to(node)

        time = distance / speed

        return time

    def steal(self):
        """
        Steals marked items form node

        :return: tuple
            Value of stolen items, weight of stolen items
        """
        value = 0
        weight = 0
        for item in self.items:
            if item.to_steal:
                value += item.value
                weight += item.weight

        return value, weight


class Item:
    """
    Item

    value - Value of the item
    weight - Weight of the item
    ratio - Value/weight ratio
    to_steal - If item will be picked
    """

    def __init__(self, value, weight):
        """
        :param value: int
            Value of item
        :param weight: int
            Weight of item
        """
        self.value = value
        self.weight = weight
        self.ratio = value / weight
        self.to_steal = False
