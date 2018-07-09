import numpy as np
import scipy.spatial.distance as ssd
import scipy.optimize as optimize
import math


class Cluster:
    def __init__(self, **kwargs):
        """
        Args:
            \**kwargs: cluster1 and cluster2 or index and demand
        """
        cluster1 = None
        cluster2 = None
        index = None
        demand = None
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "cluster1":
                    cluster1 = value
                elif key == "cluster2":
                    cluster2 = value
                elif key == "demand":
                    demand = value
                elif key == "index":
                    index = value

        if not type(cluster1) is Cluster or not type(cluster2) is Cluster:
            if index is not None and demand is not None:
                self.cluster_indices = [index]
                self.demand = demand
            else:
                raise AttributeError("Two cluster or demand and index must be given as arguments")
        else:
            self.subcluster =(cluster1, cluster2)
            self.demand = cluster1.demand + cluster2.demand
            self.cluster_indices = cluster1.cluster_indices + cluster2.cluster_indices

    def __repr__(self):
        return "Cluster: {}, demand: {}".format(self.cluster_indices, self.demand)


class HierarchicalClustering:
    def __init__(self, distances, demands):
        """
        Args:
            distances(ndarray): distance matrix
        """
        self.customer_count = distances.shape[0]
        self.distances = distances
        self.demands = demands
        print(distances)

    def _initial_clusters(self):
        clusters = []
        for i, demand in enumerate(self.demands):
            clusters.append(Cluster(index=i, demand=demand))
        return clusters

    def cluster(self):
        clusters = self._initial_clusters()
        cluster_distances = np.array(self.distances)
        # convert the redundant n*n square matrix form into a condensed nC2 array
        # flattened_distances[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
        flattened_distances = ssd.squareform(cluster_distances)
        while len(clusters) > 1:
            nearest_cluster_index = np.argmin(flattened_distances)
            cluster1_index, cluster2_index = self._flattened_index_to_two_d(nearest_cluster_index)
            break

    def _calculate_start_index_of_row(self, row):
        return row * self.customer_count - (row * (row + 1)) / 2

    def _flattened_index_to_two_d(self, index):
        very_small = 0.000000001  # to prevent strange rounding
        row = math.floor(optimize.fsolve(lambda x: self._calculate_start_index_of_row(x) - index, np.array([0]))[0]
                         + very_small)
        column = math.floor(index - self._calculate_start_index_of_row(row) + row + 1 + very_small)
        return row, column

    def _two_d_to_flattened_index(self, row, column):
        if row >= column:
            raise AttributeError("column must be greater than row for upper triangle in matrix")
        return self._calculate_start_index_of_row(row) + column - row


def symmetric_distance_matrix(distances):
    symmetric = np.copy(distances)
    n = distances.shape[0]
    if distances.shape[1] != n:
        raise AttributeError("Not quadratic")
    for x in range(n):
        for y in range(n):
            first = distances[x, y]
            second = distances[y, x]
            if first != second:
                mean = np.mean([first, second])
                symmetric[x, y] = mean
                symmetric[y, x] = mean
    return symmetric


if __name__ == '__main__':
    cluster1 = Cluster(index=0, demand=20)
    cluster2 = Cluster(index=5, demand=4)
    cluster3 = Cluster(cluster1=cluster1, cluster2=cluster2)
    print(cluster1, cluster2, cluster3)
    path = "../Vehicle_Routing_Problems/VRP1/"
    distances = np.loadtxt(path + "distance.txt")
    distances = symmetric_distance_matrix(distances)
    demands = np.loadtxt(path + "demand.txt", dtype=int)
    test_city_count = 7
    HC = HierarchicalClustering(distances[0:test_city_count, 0:test_city_count], demands[0:test_city_count])
    HC.cluster()
    # from scipy.special import comb
    # print([[comb(4, 2)-comb(4-i,2)+j-i for j in range(4)] for i in range(4)])

