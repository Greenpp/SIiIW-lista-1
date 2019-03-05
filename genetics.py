import random


class Genotype:
    """
    Genotype representing encoded path between nodes

    nodes_order - Order of visited nodes
    """

    def __init__(self, nodes_num):
        """
        :param nodes_num: int
            Total number of nodes
        """
        self.nodes_order = list(range(nodes_num))
        random.shuffle(self.nodes_order)

    def decode(self):
        """
        Decodes genotype to phenotype

        :return: list
            List of nodes pairs in traversal order
        """
        phenotype = list(zip(self.nodes_order[:-1], self.nodes_order[1:]))
        phenotype.append((self.nodes_order[-1], self.nodes_order[0]))

        return phenotype
