import unittest
import numpy as np
from Final.HierarchicalCluster import HierarchicalClustering, VRPHierarchicalClustering, d_max, d_min


class HierarchicalClusteringTest(unittest.TestCase):
    """ Test for testing the HierarchicalCluster and the VRPHierarchicalCluster"""
    def setUp(self):
        distances = np.array([[0, 1, 4, 6.5, 8.5],
                     [1, 0, 3, 5.5, 7.5],
                     [4, 3, 0, 2.5, 4.5],
                     [6.5, 5.5, 2.5, 0, 2],
                     [8.5, 7.5, 4.5, 2, 0]])
        self.testClustering1 = HierarchicalClustering(distances)
        self.testClustering2 = VRPHierarchicalClustering(distances, [i for i in range(1, 6)])

    def test_clustering_single_linkage(self):
        cluster = self.testClustering1.cluster(d_min)
        print(cluster.as_tree())
        subclu1, subclu2 = cluster.subclusters
        self.assertEqual([0, 1], subclu1.cluster_indices)
        self.assertEqual([2, 3, 4], subclu2.cluster_indices)

        cluster = self.testClustering2.cluster(d_min)
        print(cluster.as_tree())
        print(cluster)
        subclu1, subclu2 = cluster.subclusters
        self.assertEqual([0, 1], subclu1.cluster_indices)
        self.assertEqual([2, 3, 4], subclu2.cluster_indices)
        self.assertEqual(15, cluster.demand)
        self.assertEqual(3, subclu1.demand)
        self.assertEqual(12, subclu2.demand)

    def test_clustering_complete_linkage(self):
        cluster = self.testClustering1.cluster(d_max)
        print(cluster.as_tree())
        subclu1, subclu2 = cluster.subclusters
        self.assertEqual([0, 1, 2], subclu1.cluster_indices)
        self.assertEqual([3, 4], subclu2.cluster_indices)

        cluster = self.testClustering2.cluster(d_max)
        print(cluster.as_tree())
        subclu1, subclu2 = cluster.subclusters
        self.assertEqual([0, 1, 2], subclu1.cluster_indices)
        self.assertEqual([3, 4], subclu2.cluster_indices)
        self.assertEqual(15, cluster.demand)
        self.assertEqual(6, subclu1.demand)
        self.assertEqual(9, subclu2.demand)


if __name__ == '__main__':
    unittest.main()

