import numpy as np
from Final.Jonathan.HierarchicalCluster import HierarchicalClustering, Cluster


class Problem:
    def __init__(self, vehicles, distances, demands):
        """
        A VehicleRoutingProblem
        Args:
            vehicles(ndarray): list of vehicles(capacity and cost)
            distances(ndarray): n*n matrix of distances between customers
            demands(ndarray): list of demands
        """
        self.vehicles = vehicles
        self.distances = distances[:100, :100]  # TODO
        self.demands = demands
        self.customer_count = len(demands)
        if self.distances.shape != (self.customer_count, self.customer_count):
            raise AttributeError("One demand per customer must be given and distance must be quadratic")


def vehicles_from_files(capacity_file, transportation_cost_file):
    caps = np.loadtxt(capacity_file, dtype=int)
    costs = np.loadtxt(transportation_cost_file, dtype=int)
    return np.vstack((caps, costs)).T


def problem_from_files(capacity_file, transportation_cost_file, demands_file, distance_file):
    vehicles = vehicles_from_files(capacity_file, transportation_cost_file)
    demands = np.loadtxt(demands_file, dtype=int)
    distances = np.loadtxt(distance_file, dtype=int)
    return Problem(vehicles, distances, demands)


class VRPAlgorithm:
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        cluster = [HierarchicalClustering(self.problem.distances, self.problem.demands).cluster()]
        vehicles = np.copy(self.problem.vehicles)
        customer_per_vehicle = np.zeros([self.problem.vehicles.shape[0], self.problem.customer_count])
        served_customers = 0
        print(customer_per_vehicle.shape)
        while served_customers < self.problem.customer_count:
            new_cluster = []
            for cl in cluster:
                v_index = self._vehicle_for_cluster(cl, vehicles)
                if v_index:
                    served_customers += len(cl.cluster_indices)
                    customer_per_vehicle[v_index][cl.cluster_indices] = True
                    vehicles[v_index][0] -= cl.demand
                else:
                    new_cluster.extend(cl.subcluster)

            cluster = new_cluster

    @staticmethod
    def _vehicle_for_cluster(cluster, vehicles):
        """
        Returns the index of the smallest vehicle with enough capacity for the given cluster
        Args:
            cluster(Cluster): the given cluster
            vehicles(ndarray): the possible vehicles
        Returns:
            (int): the index of the according vehicle or None if no vehicle is large enough
        """
        biggest = np.max(vehicles[:, 0])
        print(biggest, cluster.demand)
        if cluster.demand > biggest:
            return None
        sufficient_cap_mask = np.where(vehicles[:, 0] > cluster.demand)
        index_of_smallest_sufficient = sufficient_cap_mask[0][np.argmin(vehicles[sufficient_cap_mask, 0])]
        return index_of_smallest_sufficient


if __name__ == '__main__':
    path = "../Vehicle_Routing_Problems/VRP1/"
    problem = problem_from_files(path + "capacity.txt", path + "transportation_cost.txt",
                                 path + "demand.txt", path + "distance.txt")
    VRPAlgorithm(problem).run()
