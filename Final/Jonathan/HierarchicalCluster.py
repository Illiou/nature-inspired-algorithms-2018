import numpy as np


# distance functions
def d_mean(x, y):
    return (x + y) / 2


def d_min(x, y):
    axis = np.argmax(x.shape)
    return np.min(np.array([x, y]), axis=axis)


def d_max(x, y):
    axis = np.argmax(x.shape)
    return np.max(np.array([x, y]), axis=axis)


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
        self.max_distance = np.max(self.distances)

    def _initial_clusters(self):
        clusters = []
        for i, demand in enumerate(self.demands):
            clusters.append(Cluster(index=i, demand=demand))
        return clusters

    def cluster(self, dist_func=d_mean):
        clusters = self._initial_clusters()
        cluster_distances = np.array(self.distances)

        def set_new_distance(i, j, dist):
            cluster_distances[i, j] = dist
            cluster_distances[j, i] = dist

        while len(clusters) > 1:
            nearest_cluster_index = np.unravel_index(np.argmin(np.where(cluster_distances != 0,
                                                                        cluster_distances, self.max_distance+1)),
                                                     cluster_distances.shape)
            print(nearest_cluster_index)
            first_cluster_index = int(nearest_cluster_index[0])
            first_cluster = clusters[first_cluster_index]
            second_cluster_index = int(nearest_cluster_index[1])
            second_cluster = clusters[second_cluster_index]
            set_new_distance(*nearest_cluster_index, 0)
            cluster_distances[first_cluster_index] = dist_func(cluster_distances[first_cluster_index],
                                                               cluster_distances[second_cluster_index])
            cluster_distances[:, first_cluster_index] = dist_func(cluster_distances[:, first_cluster_index],
                                                                  cluster_distances[:, second_cluster_index])

            mask_second_out = np.arange(cluster_distances.shape[0]) != second_cluster_index
            cluster_distances = cluster_distances[mask_second_out]
            cluster_distances = cluster_distances[:, mask_second_out]
            clusters[first_cluster_index] = Cluster(cluster1=first_cluster, cluster2=second_cluster)
            clusters = clusters[:second_cluster_index] + clusters[second_cluster_index+1:]
            print(clusters)
            print(cluster_distances)
        return clusters


if __name__ == '__main__':
    cluster1 = Cluster(index=0, demand=20)
    cluster2 = Cluster(index=5, demand=4)
    cluster3 = Cluster(cluster1=cluster1, cluster2=cluster2)
    print(cluster1, cluster2, cluster3)
    path = "../Vehicle_Routing_Problems/VRP1/"
    distances = np.loadtxt(path + "distance.txt")
    demands = np.loadtxt(path + "demand.txt", dtype=int)
    test_city_count = 9
    HC = HierarchicalClustering(distances[0:test_city_count, 0:test_city_count], demands[0:test_city_count])
    HC.cluster()
    HC.cluster(dist_func=d_min)
    HC.cluster(dist_func=d_max)

