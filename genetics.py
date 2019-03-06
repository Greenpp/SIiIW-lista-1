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

    def mutation_swap(self):
        """
        Mutation swaps two random nodes
        """
        # positions to swap
        pos1, pos2 = random.sample(range(len(self.nodes_order)), 2)

        tmp = self.nodes_order[pos1]
        self.nodes_order[pos1] = self.nodes_order[pos2]
        self.nodes_order[pos2] = tmp

    def mutation_inverse(self):
        """
        Mutation inverses genotype fragment
        """
        # beginning and end of fragment to inverse
        pos1, pos2 = sorted(random.sample(range(len(self.nodes_order)), 2))

        # inverse <pos1, pos2>
        for i, v in zip(range(pos2 - pos1 + 1), reversed(self.nodes_order[pos1:pos2 + 1])):
            self.nodes_order[pos1 + i] = v
