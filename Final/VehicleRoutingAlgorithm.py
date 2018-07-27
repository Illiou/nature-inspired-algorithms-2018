import numpy as np
from Final.HierarchicalCluster import HierarchicalClustering, Cluster
from Final.Solution import Solution
from Final.TSPACO import TSPACO

# ant parameters TODO
INITIALIZATION_VALUE = 5
EVAPORATION_RATE = 0.02
INTENSIFICATION_VALUE = 0.6
ITERATIONS = 1200
ALPHA = 1
BETA = 6
ANT_NUMBER = 100
N_BEST_TO_INTENSIFY = 3


class Problem:
    def __init__(self, vehicles, distances, demands, max_allowed_value=None):
        """
        A VehicleRoutingProblem
        Args:
            vehicles(ndarray): list of vehicles(capacity and cost)
            distances(ndarray): n*n matrix of distances between customers and depot
            demands(ndarray): list of demands
        """
        self.vehicles = vehicles
        self.distances = distances
        self.demands = demands
        self.max_allowed_value = max_allowed_value
        self.customer_count = len(demands)
        if self.distances.shape != (self.customer_count + 1, self.customer_count + 1):
            raise AttributeError("One demand per customer must be given and distance must be quadratic")


def vehicles_from_files(capacity_file, transportation_cost_file):
    caps = np.loadtxt(capacity_file, dtype=int)
    costs = np.loadtxt(transportation_cost_file, dtype=int)
    return np.vstack((caps, costs)).T


def problem_from_files(capacity_file, transportation_cost_file, demands_file, distance_file, max_value_file):
    vehicles = vehicles_from_files(capacity_file, transportation_cost_file)
    demands = np.loadtxt(demands_file, dtype=int)
    distances = np.loadtxt(distance_file, dtype=int)
    max_allowed_value = np.loadtxt(max_value_file, dtype=int)
    return Problem(vehicles, distances, demands, max_allowed_value)


class VRPAlgorithm:
    def __init__(self, problem):
        self.problem = problem
        self.customer_per_vehicle = None

    def run(self):
        self.customer_per_vehicle = self.calculate_customer_per_vehicle(inner_distance_ratio_bound=0.57)
        print(self.customer_per_vehicle)
        permutation_for_vehicles = self.calculate_permutation_for_vehicles()
        print(permutation_for_vehicles)
        solution = Solution(*zip(*permutation_for_vehicles))
        solution.cost = self.objective_function(solution)
        return solution

    def calculate_permutation_for_vehicles(self):  # TODO test 1 customer in vehicle
        customer_count_per_vehicle = np.sum(self.customer_per_vehicle, axis=1)
        vehicle_count = self.problem.vehicles.shape[0]
        permutation_per_vehicle = [([0], 0)] * vehicle_count
        # every vehicle visits depot
        vehicle_visits_at_least_one = customer_count_per_vehicle > 1
        for i, vehicle_customers in enumerate(self.customer_per_vehicle[vehicle_visits_at_least_one]):
            nonzero_indices = vehicle_customers.nonzero()[0]
            distances = self.problem.distances[np.ix_(nonzero_indices, nonzero_indices)]
            aco = TSPACO(distances, INITIALIZATION_VALUE, EVAPORATION_RATE, INTENSIFICATION_VALUE, ALPHA, BETA,
                         ANT_NUMBER, N_BEST_TO_INTENSIFY)
            best_paths, best_paths_lengths = aco.run(ITERATIONS)
            vehicle_index = np.arange(vehicle_count)[vehicle_visits_at_least_one][i]
            permutation_per_vehicle[vehicle_index] = (best_paths[-1], best_paths_lengths[-1])
        return permutation_per_vehicle

    def calculate_customer_per_vehicle(self, inner_distance_ratio_bound=None):
        cluster = [HierarchicalClustering(self.problem.distances[1:, 1:], self.problem.demands).cluster()]
        vehicles = np.copy(self.problem.vehicles)
        customer_per_vehicle = np.zeros([self.problem.vehicles.shape[0], self.problem.customer_count])
        served_customers = 0
        inner_distance_bound = np.mean(self.problem.distances) \
                               * inner_distance_ratio_bound if inner_distance_ratio_bound else None
        while served_customers < self.problem.customer_count:
            new_cluster = []
            for cl in cluster:
                if inner_distance_ratio_bound \
                        and cl.inner_distance(self.problem.distances[1:, 1:]) > inner_distance_bound:
                    new_cluster.extend(cl.subcluster)
                    continue
                v_index = self._vehicle_for_cluster(cl, vehicles)
                if v_index:
                    served_customers += len(cl.cluster_indices)
                    customer_per_vehicle[v_index][cl.cluster_indices] = True
                    vehicles[v_index][0] -= cl.demand
                else:
                    if not cl.subcluster:
                        raise ValueError(f"No solution found. The inner_distance_bound "
                                         f"{inner_distance_ratio_bound} might be too low")
                    new_cluster.extend(cl.subcluster)

            cluster = new_cluster
        customer_per_vehicle = np.concatenate((np.ones((customer_per_vehicle.shape[0], 1)), customer_per_vehicle),
                                              axis=1)
        return customer_per_vehicle

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
        if cluster.demand > biggest:
            return None
        sufficient_cap_mask = np.where(vehicles[:, 0] > cluster.demand)
        index_of_smallest_sufficient = sufficient_cap_mask[0][np.argmin(vehicles[sufficient_cap_mask, 0])]
        return index_of_smallest_sufficient

    def objective_function(self, solution):
        return np.dot(self.problem.vehicles[:, 1], solution.solution_lengths)


if __name__ == '__main__':
    problem_number = 1
    path = f"./Vehicle_Routing_Problems/VRP{problem_number}/"
    problem = problem_from_files(path + "capacity.txt", path + "transportation_cost.txt",
                                 path + "demand.txt", path + "distance.txt",
                                 path + "should_be_better_than_value.txt")
    solution = VRPAlgorithm(problem).run()
    print(solution)
    print(solution.cost)
    print(solution.solution_lengths)
