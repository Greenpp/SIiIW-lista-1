from genetics import Genotype


class Entity:
    def __init__(self, nodes_num=None):
        self.genotype = None if nodes_num is None else Genotype(nodes_num)


class Node:
    def __init__(self, x, y):
        self.position = (x, y)
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Item:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight
