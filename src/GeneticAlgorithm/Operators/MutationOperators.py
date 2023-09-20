import numpy as np


class MutationOperators:
    @staticmethod
    def swap_mutation(genes, start, end):
        genes[start], genes[end] = genes[end], genes[start]
        return genes

    @staticmethod
    def scramble_mutation(genes, start, end):
        genes = np.array(genes)
        scrambled_order = np.random.choice(np.arange(start, end), end - start)
        genes[start:end] = genes[scrambled_order]
        return genes.tolist()

    @staticmethod
    def rotation_mutation(genes, start, end):
        no_of_reverse = end - start + 1
        count = 0
        while no_of_reverse // 2 != count:
            genes[start + count], genes[end - count] = genes[end - count], genes[start + count]
            count += 1
        return genes

    @staticmethod
    def inversion_mutation(genes, start, end):
        for i in range(start, (start + end) // 2 + 1):
            genes[i], genes[start + end - i] = genes[start + end - i], genes[i]
        return genes
