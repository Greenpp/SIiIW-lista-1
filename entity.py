from genetics import Genotype


class Entity:
    """
    Entity representing single path

    genotype - Encoded path
    fitness - Score of this path
    """

    def __init__(self, nodes_num=None):
        self.genotype = None if nodes_num is None else Genotype(nodes_num)
        self.fitness = None

    def test(self, nodes, max_speed, min_speed):
        self.fitness = 0
        weight = 0
        path = self.genotype.decode()

        for id1, id2 in path:
            node1 = nodes[id1]
            node2 = nodes[id2]

            # TODO steal from node 1, calculate value and speed
            value = 0
            # TODO speed base on weight
            speed = max_speed
            time = node1.calculate_time_to(node2, speed)
            self.fitness += value
            self.fitness -= time


class Node:
    """
    Node representing city

    position - Coordinates of the city
    items - Items aviable in the city
    """

    def __init__(self, x, y):
        self.position = (x, y)
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_time_to(self, node, speed):
        x1, y1 = self.position
        x2, y2 = node.position

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

        time = distance / speed

        return time


class Item:
    """
    Item

    profit - Value of the item
    weight - Weight of the item
    """

    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight
