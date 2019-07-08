import numpy as np


# distance functions
def d_mean(x, y):
    """ Returns the mean of x and y"""
    return (x + y) / 2


def d_min(x, y):
    """ Returns the smaller value of of x and y"""
    axis = np.argmax(x.shape)
    return np.min(np.array([x, y]), axis=axis)


def d_max(x, y):
    """ Returns the bigger value of of x and y"""
    axis = np.argmax(x.shape)
    return np.max(np.array([x, y]), axis=axis)


class Cluster:
    def __init__(self, **kwargs):
        """
        A cluster, which consists of either an index for a single data point or of two subclusters
        Args:
            **kwargs: cluster1(Cluster) and cluster2(Cluster) or index(int)
        """
        cluster1 = None
        cluster2 = None
        index = None
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "cluster1":
                    cluster1 = value
                elif key == "cluster2":
                    cluster2 = value
                elif key == "index":
                    index = value

        if not issubclass(type(cluster1), Cluster)or not issubclass(type(cluster2), Cluster):
            if index is not None:
                self.cluster_indices = [index]
                self.subclusters = None
            else:
                raise AttributeError("Two cluster or index must be given as arguments for Cluster")
        else:
            self.subclusters = (cluster1, cluster2)
            self.cluster_indices = cluster1.cluster_indices + cluster2.cluster_indices

    def inner_distance(self, distances):
        """
        Calculates the inner distance (the average distance between points in the cluster)
        Args:
            distances(ndarray): the distance matrix containing all distances of the current space
        Returns:
            (number): the average inner distance
        """
        cluster_distances = distances[np.ix_(self.cluster_indices, self.cluster_indices)]
        number_of_connections = np.power(cluster_distances.shape[0] - 1, 2)
        return np.sum(cluster_distances) // number_of_connections if number_of_connections > 0 else 0

    def __repr__(self):
        return "Cluster: {}".format(self.cluster_indices)

    def as_tree(self, layer=0, margin_steps=None):
        """
        Returns the cluster as a printable tree like string
        Args:
            layer(int): for the recursive calling only - the number of the layer we are in at the moment
            margin_steps(int): the size of the margin
        Returns:
            (str) the tree-string
        """
        if not margin_steps:
            margin_steps = int(len(self.cluster_indices) / 1.5)
        margin = "\t" * margin_steps * layer
        tree_string = margin + str(self.cluster_indices)
        if not self.subclusters:
            return tree_string
        tree_string = self.subclusters[0].as_tree(layer + 1, margin_steps) + "\n" + tree_string + "\n"
        tree_string += self.subclusters[1].as_tree(layer + 1, margin_steps)
        return tree_string


class VRPCluster(Cluster):
    def __init__(self, **kwargs):
        """
        A VRPCluster which is a Cluster with an additional demand
        Args:
            **kwargs:
        """
        super(VRPCluster, self).__init__(**kwargs)
        if self.subclusters is None:
            if "demand" in kwargs:
                self.demand = kwargs.get("demand")
            else:
                raise AttributeError("Two cluster or index and demand must be given as arguments for VRPCluster")
        else:
            self.demand = self.subclusters[0].demand + self.subclusters[1].demand

        def __repr__(self):
            return "VRPCluster: {}, {}".format(self.cluster_indices, self.demand)


class HierarchicalClustering:
    def __init__(self, distances):
        """
        Class for clustering point according to the given distances
        Args:
            distances(ndarray): distance matrix with distance from each point to each other point
        """
        self.point_count = distances.shape[0]
        self.distances = distances
        self.max_distance = np.max(self.distances)

    def _initial_clusters(self):
        """
        Creates the initial clusters, one for each point
        Returns: (list(Cluster)) the list of clusters
        """
        clusters = []
        for i in range(self.point_count):
            clusters.append(self._create_cluster_from_index(i))
        return clusters

    def _create_cluster_from_index(self, index):
        """
        Creates a cluster for the given index
        Args:
            index(int): the index
        Returns: (Cluster) The created cluster
        """
        return Cluster(index=index)

    def _create_from_subclusters(self, cluster1, cluster2):
        """
        Creates a cluster of the given subclusters
        Args:
            cluster1(Cluster): the first cluster
            cluster2(Cluster): the second cluster
        Returns: (Cluster) The created cluster
        """
        return Cluster(cluster1=cluster1, cluster2=cluster2)

    def cluster(self, dist_func=d_mean):
        clusters = self._initial_clusters()
        cluster_distances = np.array(self.distances)

        def set_new_distance(i, j, dist):
            cluster_distances[i, j] = dist
            cluster_distances[j, i] = dist

        while len(clusters) > 1:
            nearest_cluster_index = np.unravel_index(np.argmin(np.where(cluster_distances != 0,
                                                                        cluster_distances, self.max_distance + 1)),
                                                     cluster_distances.shape)
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
            clusters[first_cluster_index] = self._create_from_subclusters(cluster1=first_cluster,
                                                                          cluster2=second_cluster)
            clusters = clusters[:second_cluster_index] + clusters[second_cluster_index + 1:]
        return clusters[0]


class VRPHierarchicalClustering(HierarchicalClustering):
    def __init__(self, distances, demands):
        super(VRPHierarchicalClustering, self).__init__(distances)
        self.demands = demands

    def _create_cluster_from_index(self, index):
        """
        Creates a cluster for the customer at the given index with the according demand
        Args:
            index(int): the index
        Returns: (VRPCluster) The created cluster
        """
        return VRPCluster(index=index, demand=self.demands[index])

    def _create_from_subclusters(self, cluster1, cluster2):
        """
        Creates a VRPCluster of the given subclusters
        Args:
            cluster1(VRPCluster): the first cluster
            cluster2(VRPCluster): the second cluster
        Returns: (VRPCluster) The created cluster
        """
        return VRPCluster(cluster1=cluster1, cluster2=cluster2)


if __name__ == '__main__':
    # Run the VRPClustering on the VRP1
    path = "./Vehicle_Routing_Problems/VRP1/"
    distances = np.loadtxt(path + "distance.txt")
    demands = np.loadtxt(path + "demand.txt", dtype=int)
    test_city_count = 100
    HC = VRPHierarchicalClustering(distances[0:test_city_count, 0:test_city_count], demands[0:test_city_count])
    cluster = HC.cluster(dist_func=d_max)
    print(cluster.demand)
    print(cluster.as_tree())
