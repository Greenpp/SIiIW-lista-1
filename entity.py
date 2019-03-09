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

    def test(self, nodes, min_speed, max_speed, max_weight):
        """
        Calculates fitness

        Used formula:
            g(y) - f(x, y)
        Where:
            g(y) - sum of stolen items
            f(x, y) - total time of traversal

        :param nodes: list
            List of all nodes
        :param max_speed: float
            Speed with empty bag
        :param min_speed: float
            Speed with full bag
        :param max_weight: int
            Capacity of bag
        """
        self.fitness = 0
        weight = 0
        path = self.genotype.decode()

        for id1, id2 in path:
            node1 = nodes[id1]
            node2 = nodes[id2]

            city_value, city_weight = node1.steal()

            weight += city_weight
            speed = max_speed - weight * (max_speed - min_speed) / max_weight
            time = node1.calculate_time_to(node2, speed)

            self.fitness += city_value
            self.fitness -= time

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
        for i in self.genotype.nodes_order:
            if nodes[i].steal() == (0, 0):
                skipped_cities.append(i)
            else:
                robbed_cities.append(i)

        g = nx.DiGraph(edges)
        layout = nx.circular_layout(g)

        # draw
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
    items - Items aviable in the city
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
        x1, y1 = self.position
        x2, y2 = node.position

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

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
