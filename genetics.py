import random


class Genotype:
    def __init__(self, nodes_num):
        self.nodes_order = list(range(nodes_num))
        random.shuffle(self.nodes_order)
