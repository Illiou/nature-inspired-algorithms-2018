import numpy as np


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
        self.distances = distances
        self.demands = demands

    def _initial_clusters(self):
        clusters = []
        for i, demand in enumerate(self.demands):
            clusters.append(Cluster(index=i, demand=demand))
        return clusters

    def cluster(self):
        clusters = self._initial_clusters()
        cluster_distances = np.array(self.distances)
        while len(clusters) > 1:
            argmin = np.argmin(cluster_distances)
            print(argmin)
            break


if __name__ == '__main__':
    cluster1 = Cluster(index=0, demand=20)
    cluster2 = Cluster(index=5, demand=4)
    cluster3 = Cluster(cluster1=cluster1, cluster2=cluster2)
    print(cluster1, cluster2, cluster3)
    path = "../Vehicle_Routing_Problems/VRP1/"
    distances = np.loadtxt(path + "distance.txt")
    demands = np.loadtxt(path + "demand.txt", dtype=int)
    print(distances.shape, sep=" ")
    HC = HierarchicalClustering(distances[0:3, 0:3], demands[0:3])
    HC.cluster()
    print(np.arange(20).reshape(5, 4))
    print(np.indices((2,3)))

