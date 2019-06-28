import numpy as np
import matplotlib.pyplot as plt
import random
from numba import jitclass
from numba import boolean, int64, float64


SHUFFLETRUCK = 0
SWAPANY = 1
SWAPADJACENT = 2
SWAPADJACENTDISTBASED = 3

spec = [
    ("distance", int64[:, :]),
    ("transportation_cost", int64[:]),
    ("capacity", int64[:]),
    ("demand", int64[:]),
    ("truck_count", int64),
    ("customer_count", int64),
    ("truck_sol_length", int64),
    ("neighbourhood", int64),
    ("swaps_per_truck", int64),
    ("swap_probability", float64),
    ("bee_count", int64),
    ("abandoned_limit", int64),
    ("minimization", boolean),
    ("store_best", boolean),
    ("solutions", int64[:, :, :]),
    ("not_changed_count", float64[:]),
    ("nectar", float64[:])
]

@jitclass(spec)
class VehicleRoutingABC:
    def __init__(self, bee_count, abandoned_limit, distance, transportation_cost, capacity, demand,
                 neighbourhood=SWAPANY, swaps_per_truck=1, swap_probability=1.):
        self.distance = distance
        self.transportation_cost = transportation_cost
        self.capacity = capacity
        self.demand = demand
        self.truck_count = len(transportation_cost)
        self.customer_count = len(demand)
        # last column of solution row denotes truck order
        self.truck_sol_length = self.customer_count + 1
        self.neighbourhood = neighbourhood
        self.swaps_per_truck = swaps_per_truck
        self.swap_probability = swap_probability

        # BEE
        self.bee_count = bee_count
        self.abandoned_limit = abandoned_limit
        self.minimization = True
        self.store_best = True

        self.not_changed_count = np.zeros(self.bee_count)
        # Numba: Cannot cast none to array(int64, 3d, A)
        # self.solutions = None
        # self.nectar = None
        self.initialize()

    def objective_function(self, solutions):
        # Numba doesn't support newaxis/None
        # if solutions.ndim == 2:
        #     solutions = solutions[np.newaxis, ...]

        obfnc_values = np.empty(len(solutions))
        # Numba: enumerate(solutions): NotImplementedError: iterating over 3D array
        for sol_num in range(len(solutions)):
            demand_left = self.demand.copy()
            demand_left_sum = demand_left.sum()
            obfnc_value = 0
            for truck in solutions[sol_num, :, -1]:
                # TODO remove if sure bug is gone
                # if len(set(solution[truck].tolist())) != 100:
                #     print("Error, duplicate element in:")
                #     print(solution[truck])
                if demand_left_sum <= 0:
                    break
                customer_list = solutions[sol_num, truck, :-1]
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
                        truck_dist += self.distance[last_customer + 1, curr_customer + 1]
                        last_customer = curr_customer
                # back to depot
                truck_dist += self.distance[last_customer + 1, 0]
                obfnc_value += truck_dist * self.transportation_cost[truck]
                demand_left_sum -= self.capacity[truck] - max(capacity_left, 0)
            # multiply by demand left to punish unsatisfying solutions but still let the algorithm see
            # an improvement by satisfying more demand
            if demand_left_sum > 0:
                obfnc_value *= 1 + demand_left_sum
            obfnc_values[sol_num] = obfnc_value
        return obfnc_values

    def random_solutions(self, count):
        sols = np.empty((count, self.truck_count, self.truck_sol_length), dtype=np.int64)
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
                # Numba: only supports parameters (low, high) or (low, high, size), not (high, size)
                rands = np.random.randint(0, self.customer_count, size=self.truck_count * 2 * self.swaps_per_truck)\
                          .reshape(self.swaps_per_truck, -1)
                rands_prob = np.random.rand(self.swaps_per_truck, self.truck_count)
                for truck in range(self.truck_count):
                    for swap in range(self.swaps_per_truck):
                        if rands_prob[swap, truck] < self.swap_probability:
                            # swap two customer's position
                            new_sols[sol, truck, rands[swap, truck]], new_sols[sol, truck, rands[swap, -(truck + 1)]] = \
                                new_sols[sol, truck, rands[swap, -(truck + 1)]], new_sols[sol, truck, rands[swap, truck]]
            elif self.neighbourhood == SWAPADJACENT:
                rands = np.random.randint(0, self.customer_count, size=self.truck_count * self.swaps_per_truck) \
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


    # BEE
    def max_or_minimizing_objective_function(self, solutions):
        values = self.objective_function(solutions)
        if self.minimization:
            return np.where(values < 0, 1 + np.abs(values), 1/(1 + values))
        else:
            return values

    def initialize(self):
        self.solutions = self.random_solutions(self.bee_count)
        self.nectar = self.max_or_minimizing_objective_function(self.solutions)

    def employed_phase(self):
        new_solutions, new_nectar = self.generate_neighbours(self.solutions)
        should_change = self.nectar < new_nectar
        # not even gonna try to make this work with Numba...
        # expand_to_sol_dim = (slice(None),) + (np.newaxis,) * (self.solutions.ndim - 1) # for n-dimensional solutions
        # self.solutions = np.where(should_change[expand_to_sol_dim], new_solutions, self.solutions)
        should_change_full = np.empty(self.solutions.shape)
        for i in range(len(should_change)):
            should_change_full[i] = should_change[i]
        self.solutions = np.where(should_change_full, new_solutions, self.solutions)
        self.nectar = np.where(should_change, new_nectar, self.nectar)
        no_change = ~ should_change
        self.not_changed_count = (self.not_changed_count + no_change) * no_change

    def onlooker_phase(self):
        probabilities = self.nectar / np.sum(self.nectar)
        # Numba doesn't support p in random.choice
        # solution_choices = np.random.choice(self.bee_count, self.bee_count, p=probabilities)
        solution_choices = np.searchsorted(probabilities.cumsum(), np.random.rand(self.bee_count), side="right")
        neighbours, neighbours_nectar = self.generate_neighbours(self.solutions[solution_choices])
        for choice in set(solution_choices):
            choice_indices = np.where(choice == solution_choices)[0]
            best_choice = choice_indices[np.argmax(neighbours_nectar[choice_indices])]
            if neighbours_nectar[best_choice] >= self.nectar[choice]:
                self.solutions[choice] = neighbours[best_choice]
                self.nectar[choice] = neighbours_nectar[best_choice]
                self.not_changed_count[choice] = 0

    def scout_phase(self, best_index=-1):
        limit_exceeded = self.not_changed_count >= self.abandoned_limit
        if best_index != -1:
            limit_exceeded[best_index] = False
        # Numba doesn't support countnonzero
        # new_solutions = self.random_solutions(np.count_nonzero(limit_exceeded))
        new_solutions = self.random_solutions(len(np.nonzero(limit_exceeded)))
        self.solutions[limit_exceeded] = new_solutions
        self.nectar[limit_exceeded] = self.max_or_minimizing_objective_function(new_solutions)

    def run(self, iterations=100):
        best_nectars = np.zeros(iterations)
        best_index = -1
        for i in range(iterations):
            if i % 100 == 0:
                print("step", i)
            self.employed_phase()
            self.onlooker_phase()
            if self.store_best:
                self.scout_phase(best_index)
            else:
                self.scout_phase(-1)
            # to not have the transformed nectar in minimization
            best_index = np.argmax(self.nectar)
            best_nectars[i] = self.objective_function(np.expand_dims(self.solutions[best_index], axis=0))[0]
        return best_nectars, self.solutions[best_index]


# def actual_solution(ABC, solution):
#     demand_left = ABC.demand.copy()
#     demand_left_sum = sum(demand_left)
#     obfnc_value = 0
#     actual_solution = [[0] for _ in range(ABC.truck_count)]
#     for truck in solution[:, -1]:
#         if demand_left_sum <= 0:
#             break
#         customer_list = solution[truck, :-1].tolist()
#         capacity_left = ABC.capacity[truck]
#         truck_dist = 0
#         last_customer = -1  # depot
#         for curr_customer in customer_list:
#             if capacity_left <= 0:
#                 break
#             if demand_left[curr_customer] > 0:
#                 actual_solution[truck].append(curr_customer)
#                 # subtract demand from truck capacity
#                 capacity_left -= demand_left[curr_customer]
#                 # if not too much demand for truck then set to 0, otherwise set to remaining demand
#                 demand_left[curr_customer] = 0 if capacity_left >= 0 else - capacity_left
#                 # add distance from last to current customer
#                 truck_dist += ABC.distance[last_customer + 1][curr_customer + 1]
#                 last_customer = curr_customer
#         # back to depot
#         truck_dist += ABC.distance[last_customer + 1][0]
#         obfnc_value += truck_dist * ABC.transportation_cost[truck]
#         demand_left_sum -= ABC.capacity[truck] - capacity_left
#     # multiply by demand left to punish unsatisfying solutions but still let the algorithm see
#     # an improvement by satisfying more demand
#     if demand_left_sum > 0:
#         obfnc_value *= 1 + demand_left_sum
#     return obfnc_value, demand_left_sum, actual_solution


if __name__ == '__main__':
    problem_num = 1
    bee_count = 100
    abandoned_limit = 50
    swaps_per_truck = 1
    swap_probability = 0.1
    iterations = 500000

    problem_path = f"Vehicle_Routing_Problems/VRP{problem_num}/"
    distance = np.loadtxt(problem_path + "distance.txt", dtype=np.int64)
    transportation_cost = np.loadtxt(problem_path + "transportation_cost.txt", dtype=np.int64)
    capacity = np.loadtxt(problem_path + "capacity.txt", dtype=np.int64)
    demand = np.loadtxt(problem_path + "demand.txt", dtype=np.int64)

    VRABC = VehicleRoutingABC(bee_count, abandoned_limit, distance, transportation_cost, capacity, demand,
                              neighbourhood=SWAPANY, swaps_per_truck=swaps_per_truck, swap_probability=swap_probability)

    np.set_printoptions(threshold=np.nan)
    best_nectars, best_solution = VRABC.run(iterations)
    print(best_nectars)
    print(best_solution)

    curr_fig, curr_ax = plt.subplots()
    curr_ax.plot(best_nectars, label="Best nectar")
    # curr_ax.axhline(benchmark, linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_num}", xlabel="Iteration", ylabel="Best objective function")
    curr_ax.legend()
    plt.show()
