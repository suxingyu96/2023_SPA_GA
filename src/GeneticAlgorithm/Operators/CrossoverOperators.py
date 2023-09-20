import copy
import numpy as np


class CrossoverOperators:
    @staticmethod
    def crossover_PMX(parentGenes, donorGenes, start, end):
        child_1 = np.array(copy.deepcopy(parentGenes))
        child_2 = np.array(copy.deepcopy(donorGenes))
        length = len(parentGenes)
        start_end_range = range(start, end)
        left = np.delete(range(length), start_end_range)

        left_parent, left_donor = child_1[left], child_2[left]
        cross_part_parent, cross_part_donor = child_1[start_end_range], child_2[start_end_range]

        child_1[start_end_range], child_2[start_end_range] = cross_part_donor, cross_part_parent

        mapping = [[], []]

        for i, j in zip(cross_part_parent, cross_part_donor):
            if j in cross_part_parent and i not in cross_part_donor:
                index = np.argwhere(cross_part_parent == j)[0, 0]
                value = cross_part_donor[index]
                while True:
                    if value in cross_part_parent:
                        index = np.argwhere(cross_part_parent == value)[0, 0]
                        value = cross_part_donor[index]
                    else:
                        break
                mapping[0].append(i)
                mapping[1].append(value)

            elif i in cross_part_donor:
                pass

            else:
                mapping[0].append(i)
                mapping[1].append(j)

        for i, j in zip(mapping[0], mapping[1]):
            if i in left_parent:
                left_parent[np.argwhere(left_parent == i)[0, 0]] = j
            elif i in left_donor:
                left_donor[np.argwhere(left_donor == i)[0, 0]] = j
            if j in left_parent:
                left_parent[np.argwhere(left_parent == j)[0, 0]] = i
            elif j in left_donor:
                left_donor[np.argwhere(left_donor == j)[0, 0]] = i

        child_1[left], child_2[left] = left_parent, left_donor
        return child_1.tolist()