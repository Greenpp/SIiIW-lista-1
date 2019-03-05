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

    def test(self, nodes, max_speed, min_speed, max_weight):
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

            # TODO steal from node 1, calculate value and speed
            value = 0
            speed = max_speed - weight * (max_speed - min_speed) / max_weight
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
        pass


class Item:
    """
    Item

    profit - Value of the item
    weight - Weight of the item
    ratio - value/weight ratio
    to_steal - if item will be picked
    """

    def __init__(self, profit, weight):
        self.value = profit
        self.weight = weight
        self.ratio = profit / weight
        self.to_steal = False
