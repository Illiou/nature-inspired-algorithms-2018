import numpy as np
from Final.Jonathan.HierarchicalCluster import HierarchicalClustering


class Vehicle:
    def __init__(self, capacity, transportation_cost):
        self.capacity = capacity
        self.transportation_cost = transportation_cost

    def __repr__(self):
        return "Vehicle: cap:{}-cost:{}".format(self.capacity, self.transportation_cost)


class Problem:
    def __init__(self, vehicles, distances, demands):
        """
        A VehicleRoutingProblem
        Args:
            vehicles(list(Vehicle)): list of vehicles
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
    return [Vehicle(cap, cost) for cap, cost in zip(caps, costs)]


def problem_from_files(capacity_file, transportation_cost_file, demands_file, distance_file):
    vehicles = vehicles_from_files(capacity_file, transportation_cost_file)
    demands = np.loadtxt(demands_file, dtype=int)
    distances = np.loadtxt(distance_file, dtype=int)
    return Problem(vehicles, distances, demands)


class VRPAlgorithm:
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        cluster = HierarchicalClustering(self.problem.distances, self.problem.demands).cluster()


if __name__ == '__main__':
    path = "../Vehicle_Routing_Problems/VRP1/"
    problem = problem_from_files(path + "capacity.txt", path + "transportation_cost.txt",
                                 path + "demand.txt", path + "distance.txt")
    VRPAlgorithm(problem).run()
