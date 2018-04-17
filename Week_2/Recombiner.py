# <<<<<<< HEAD
# from AbstractModules import AbstractRecombiner
# import random
#
# class KPointCrossover(AbstractRecombiner):
#
#     def recombine(parents):
#         k = 2
#         crossover_points = [0]
#         crossover_points.append(random.randint(0, k-1))
#
#         children = []
#         for i in range(1, len(crossover_points)):
#             new_child = []
#             for j in range(len(crossover_points+1)):
#                 parent = parents[j%len(parents)]
#                 new_child.append(parent[crossover_points[i-1]:crossover_points[i]])
#             children.append(new_child)
#
#         return children
# =======
from Week_2.AbstractModules import AbstractRecombiner
from Week_2.Problem import Individual
import random


class OnePointCrossoverRecombiner(AbstractRecombiner):
    def __init__(self, parent_count):
        if parent_count != 2:
            raise AssertionError("Parent_count in OnePointCrossover must be 2")
        super().__init__(parent_count)

    def recombine(self, parents):
        point = random.randint(1, len(parents) - 1)
        child1 = parents[0].chromosome[:point]
        child1.extend(parents[1].chromosome[point:])
        child2 = parents[1].chromosome[:point]
        child2.extend(parents[0].chromosome[point:])
        return [Individual(parents[0].problem, child1), Individual(parents[0].problem, child2)]



>>>>>>> d6322a11bf03453c031811da1400ef1babe91c2e
