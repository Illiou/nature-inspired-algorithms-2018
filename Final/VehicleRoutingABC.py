import numpy as np
# import matplotlib.pyplot as plt
import random
from ArtificialBeeAlgorithm import ArtificialBeeColony
from AbstractVehicleRoutingAlgorithm import AbstractVehicleRoutingAlgorithm
from Solution import Solution


SHUFFLETRUCK = 0
SWAPANY = 1
SWAPADJACENT = 2
SWAPADJACENTDISTBASED = 3


def actual_solution(ABC, solution):
    """
    Calculates the real Solution from the ABC-Solution,
    by cutting paths if the trucks have brought all their load to customers
    Args:
        ABC(VehicleRoutingABC): the VehicleRoutingABC algorithm
        solution(ndarray):  the solution of the abc algorithm

    Returns: (float, list(float), list(list(int)) the objective function value for this solution(hence the cost),
    the list of driven distances per truck and the tsp_solutions for the trucks

    """
    demand_left = ABC.demand.copy()
    demand_left_sum = sum(demand_left)
    obfnc_value = 0
    tsp_solutions = [[0] for _ in range(ABC.truck_count)]
    driven_distances = [0 for _ in range(ABC.truck_count)]
    for truck_idx in solution[:, -1]:
        if demand_left_sum <= 0:
            break
        customer_list = solution[truck_idx, :-1].tolist()
        capacity_left = ABC.capacity[truck_idx]
        truck_dist = 0
        last_customer = -1  # depot
        for curr_customer in customer_list:
            if capacity_left <= 0:
                break
            if demand_left[curr_customer] > 0:
                tsp_solutions[truck_idx].append(curr_customer)
                # subtract demand from truck capacity
                capacity_left -= demand_left[curr_customer]
                # if not too much demand for truck then set to 0, otherwise set to remaining demand
                demand_left[curr_customer] = 0 if capacity_left >= 0 else - capacity_left
                # add distance from last to current customer
                truck_dist += ABC.distance[last_customer + 1][curr_customer + 1]
                last_customer = curr_customer
        # back to depot
        truck_dist += ABC.distance[last_customer + 1][0]
        obfnc_value += truck_dist * ABC.transportation_cost[truck_idx]
        demand_left_sum -= ABC.capacity[truck_idx] - capacity_left
        driven_distances[truck_idx] = truck_dist
    # multiply by demand left to punish unsatisfying solutions but still let the algorithm see
    # an improvement by satisfying more demand
    if demand_left_sum > 0:
        obfnc_value *= 1 + demand_left_sum
    return obfnc_value, driven_distances, tsp_solutions


class VehicleRoutingABC(ArtificialBeeColony, AbstractVehicleRoutingAlgorithm):
    def __init__(self, bee_count, abandoned_limit, distance, transportation_cost, capacity, demand,
                 neighbourhood=SWAPANY, swaps_per_truck=1, swap_probability=1., iterations=100):
        self.distance = distance.tolist() if isinstance(distance, np.ndarray) else distance
        self.transportation_cost = transportation_cost.tolist() if isinstance(transportation_cost, np.ndarray)\
                                   else transportation_cost
        self.capacity = capacity.tolist() if isinstance(capacity, np.ndarray) else capacity
        self.demand = demand.tolist() if isinstance(demand, np.ndarray) else demand
        self.truck_count = len(transportation_cost)
        self.customer_count = len(demand)
        # last column of solution row denotes truck order
        self.truck_sol_length = self.customer_count + 1
        self.neighbourhood = neighbourhood
        self.swaps_per_truck = swaps_per_truck
        self.swap_probability = swap_probability
        self.iterations = iterations
        lower_bounds = []
        upper_bounds = []
        super().__init__(bee_count, abandoned_limit, lower_bounds, upper_bounds, minimization=True)

    def objective_function(self, solutions):
        if solutions.ndim == 2:
            solutions = solutions[np.newaxis, ...]

        obfnc_values = np.empty(len(solutions))
        for sol_num, solution in enumerate(solutions):
            demand_left = self.demand.copy()
            demand_left_sum = sum(demand_left)
            obfnc_value = 0
            for truck in solution[:, -1]:
                # TODO remove if sure bug is gone
                # if len(set(solution[truck].tolist())) != 100:
                #     print("Error, duplicate element in:")
                #     print(solution[truck])
                if demand_left_sum <= 0:
                    break
                customer_list = solution[truck, :-1].tolist()
                capacity_left = self.capacity[truck]
                truck_dist = 0
                last_customer = -1  # depot
                for curr_customer in customer_list:
                    if capacity_left <= 0:
                        break
                    if demand_left[curr_customer] > 0:
                        # subtract demand from truck capacity
                        capacity_left -= demand_left[curr_customer]
                        # if not too much demand for truck then set to 0, otherwise set to remaining demand
                        demand_left[curr_customer] = 0 if capacity_left >= 0 else - capacity_left
                        # add distance from last to current customer
                        truck_dist += self.distance[last_customer + 1][curr_customer + 1]
                        last_customer = curr_customer
                # back to depot
                truck_dist += self.distance[last_customer + 1][0]
                obfnc_value += truck_dist * self.transportation_cost[truck]
                demand_left_sum -= self.capacity[truck] - max(capacity_left, 0)
            # multiply by demand left to punish unsatisfying solutions but still let the algorithm see
            # an improvement by satisfying more demand
            if demand_left_sum > 0:
                obfnc_value *= 1 + demand_left_sum
            obfnc_values[sol_num] = obfnc_value
        return obfnc_values

    def random_solutions(self, count):
        sols = np.empty((count, self.truck_count, self.truck_sol_length), dtype=int)
        for sol in range(count):
            for truck in range(self.truck_count):
                sols[sol, truck, :-1] = np.random.permutation(self.customer_count)
            sols[sol, :, -1] = np.random.permutation(self.truck_count)
        return sols

    def generate_neighbours(self, solutions):
        new_sols = solutions.copy()
        for sol in range(solutions.shape[0]):
            if self.neighbourhood == SHUFFLETRUCK:
                np.random.shuffle(new_sols[sol, random.randrange(self.truck_count), :-1])
            elif self.neighbourhood == SWAPANY:
                rands = np.random.randint(self.customer_count, size=self.truck_count * 2 * self.swaps_per_truck)\
                          .reshape(self.swaps_per_truck, -1)
                rands_prob = np.random.rand(self.swaps_per_truck, self.truck_count)
                for truck in range(self.truck_count):
                    for swap in range(self.swaps_per_truck):
                        if rands_prob[swap, truck] < self.swap_probability:
                            # swap two customer's position
                            new_sols[sol, truck, rands[swap, truck]], new_sols[sol, truck, rands[swap, -(truck + 1)]] = \
                                new_sols[sol, truck, rands[swap, -(truck + 1)]], new_sols[sol, truck, rands[swap, truck]]
            elif self.neighbourhood == SWAPADJACENT:
                rands = np.random.randint(self.customer_count, size=self.truck_count * self.swaps_per_truck) \
                          .reshape(self.swaps_per_truck, -1)
                rands_prob = np.random.rand(self.swaps_per_truck, self.truck_count)
                for truck in range(self.truck_count):
                    for swap in range(self.swaps_per_truck):
                        if rands_prob[swap, truck] < self.swap_probability:
                            new_sols[sol, truck, rands[swap, truck]],\
                            new_sols[sol, truck, (rands[swap, truck] + 1) % self.customer_count] = \
                                new_sols[sol, truck, (rands[swap, truck] + 1) % self.customer_count],\
                                new_sols[sol, truck, rands[swap, truck]]
            # swap position of two trucks
            if random.random() < self.swap_probability:
                left, right = random.randrange(self.truck_count), random.randrange(self.truck_count)
                new_sols[sol, left, -1], new_sols[sol, right, -1] = new_sols[sol, right, -1], new_sols[sol, left, -1]
        return new_sols, self.max_or_minimizing_objective_function(new_sols)

    def run(self, **kwargs):
        iterations = self.iterations
        if "iterations" in kwargs:
            iterations = kwargs["iterations"]
        best_nectars, best_solution = super().run(iterations)
        cost, driven_distances, tsp_solutions = actual_solution(self, best_solution)
        print(driven_distances)
        print(tsp_solutions)
        solution = Solution(tsp_solutions, driven_distances)
        solution.cost = cost
        return solution


if __name__ == '__main__':
    problem_num = 1
    bee_count = 100
    abandoned_limit = 50
    swaps_per_truck = 1
    swap_probability = 0.5
    iterations = 1000

    problem_path = f"Vehicle_Routing_Problems/VRP{problem_num}/"
    distance = np.loadtxt(problem_path + "distance.txt", dtype=np.int64)
    transportation_cost = np.loadtxt(problem_path + "transportation_cost.txt", dtype=np.int64)
    capacity = np.loadtxt(problem_path + "capacity.txt", dtype=np.int64)
    demand = np.loadtxt(problem_path + "demand.txt", dtype=np.int64)

    VRABC = VehicleRoutingABC(bee_count, abandoned_limit, distance, transportation_cost, capacity, demand,
                              neighbourhood=SWAPANY, swaps_per_truck=swaps_per_truck, swap_probability=swap_probability,
                              iterations=iterations)

    # np.set_printoptions(threshold=np.nan)
    solution = VRABC.run()
    print(solution)
    print(solution.cost)
    # print(best_nectars)
    # print(best_solution)
    #
    # curr_fig, curr_ax = plt.subplots()
    # curr_ax.plot(best_nectars, label="Best nectar")
    # # curr_ax.axhline(benchmark, linestyle="dashed", label="Benchmark")
    # curr_ax.set(title=f"Problem {problem_num}", xlabel="Iteration", ylabel="Best objective function")
    # curr_ax.legend()
    # plt.show()
