from AbstractModules import AbstractRecombiner
import random

class KPointCrossover(AbstractRecombiner):

    def recombine(self, parents):

        k = 2
        crossover_points = [0]
        for points in range(k):
            crossover_points.extend([random.randint(1, len(parents[0])-1)])
        crossover_points.sort()
        crossover_points.extend([len(parents[0])])
        #crossover_points = [0,2,5,len(parents[0])]
        #crossover_points = [0,2,len(parents[0])]
        print(crossover_points)

        children = []
        for i in range(len(parents)):
            new_child = []
            for j in range(k+1):
                parent = parents[(i+j)%len(parents)]
                #print(parent[crossover_points[j]:crossover_points[j+1]])
                #print(crossover_points[j], crossover_points[j+1])
                new_child.extend(parent[crossover_points[j]:crossover_points[j+1]])
            children.append(new_child)

        return children


class UniformScanCrossover(AbstractRecombiner):

    def recombine(self, parents):

        possibilites = [*zip(*parents)]
        #print(possibilites)

        children = []
        for i in range(len(parents)):
            children.append([random.choice(possible) for possible in possibilites])

        return children


# from Week_2.AbstractModules import AbstractRecombiner
# from Week_2.Problem import Individual
# import random
#
#
# class OnePointCrossoverRecombiner(AbstractRecombiner):
#     def __init__(self, parent_count):
#         if parent_count != 2:
#             raise AssertionError("Parent_count in OnePointCrossover must be 2")
#         super().__init__(parent_count)
#
#     def recombine(self, parents):
#         point = random.randint(1, len(parents) - 1)
#         child1 = parents[0].chromosome[:point]
#         child1.extend(parents[1].chromosome[point:])
#         child2 = parents[1].chromosome[:point]
#         child2.extend(parents[0].chromosome[point:])
#         return [Individual(parents[0].problem, child1), Individual(parents[0].problem, child2)]
#
#
#
# >>>>>>> d6322a11bf03453c031811da1400ef1babe91c2e
