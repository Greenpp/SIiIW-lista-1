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


class Item:
    """
    Item

    profit - Value of the item
    weight - Weight of the item
    """

    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight
