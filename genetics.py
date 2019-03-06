import random


class Genotype:
    """
    Genotype representing encoded path between nodes

    nodes_order - Order of visited nodes
    """

    def __init__(self, nodes_num=None):
        """
        :param nodes_num: int, optional
            Total number of nodes
        """
        self.nodes_order = list(range(nodes_num)) if nodes_num is not None else None
        if nodes_num is not None:
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

    def mutate(self, method='swap'):
        """
        Mutates genotype with given method

        :param method: str, optional
            Name of the mutation
        """
        mutations = {'swap': self.mutation_swap,
                     'inverse': self.mutation_inverse}

        if method not in mutations:
            print('Mutation type error')
            exit(1)

        mutations[method]()

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

    def crossover(self, genotype, method='simple'):
        """
        Executes given type of crossover

        :param genotype: Genotype
            Parent 2
        :param method: str, optional
            Type of crossover
        :return: Genotype
            Child
        """
        crossovers = {'simple': self.crossover_simple}

        if method not in crossovers:
            print('Crossover type error')
            exit(1)

        return crossovers[method](genotype)

    def crossover_simple(self, genotype):
        """
        Simple crossover, cuts both genotypes in random place, then creates child with p1p2 parts
        After concatenation genotype is checked for redundant nodes which are replaced with missing ones
            p1 - parent 1
            p2 - parent 2
        :param genotype: Genotype
            Parent 2
        :return: Genotype
            Child genotype
        """
        pos = random.choice(range(len(self.nodes_order)))

        child_order = self.nodes_order[:pos] + genotype.nodes_order[pos:]

        # fix
        # find redundant nodes indices
        child_nodes = set()
        idx_to_fix = []
        for i, node in enumerate(child_order):
            if node not in child_nodes:
                child_nodes.add(node)
            else:
                idx_to_fix.append(i)

        if len(idx_to_fix) > 0:
            # if any redundant nodes fix in random order
            random.shuffle(idx_to_fix)

            # calculate missing nodes
            all_nodes = set(self.nodes_order)
            missing_nodes = all_nodes.difference(child_nodes)

            for i, n in zip(idx_to_fix, missing_nodes):
                child_order[i] = n

        child_genotype = Genotype()
        child_genotype.nodes_order = child_order

        return child_genotype
