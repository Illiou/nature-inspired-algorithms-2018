import numpy as np
import matplotlib.pyplot as plt
import random
from ArtificialBeeAlgorithm import ArtificialBeeColony


SHUFFLETRUCK = 0
SWAPANY = 1
SWAPADJACENT = 2
SWAPADJACENTDISTBASED = 3

AMOUNT = 0
ORDER = 1

class VehicleRoutingABC(ArtificialBeeColony):
    """
    Solution structure:
        Truck 1
            Amount delivered to customer, by index.
            Permutation of customers, by number at position.
        Truck 2
        ...
        n + 1 entry
            Demand left for each customer.
            empty.

    """
    def __init__(self, bee_count, abandoned_limit, distance, transportation_cost, capacity, demand,
                 neighbourhood=SWAPANY, swaps_per_truck=1, swap_probability=1.):
        self.distance = distance.tolist() if isinstance(distance, np.ndarray) else distance
        self.transportation_cost = transportation_cost.tolist() if isinstance(transportation_cost, np.ndarray)\
                                   else transportation_cost
        self.capacity = capacity.tolist() if isinstance(capacity, np.ndarray) else capacity
        self.demand = demand.tolist() if isinstance(demand, np.ndarray) else demand
        self.truck_count = len(transportation_cost)
        self.customer_count = len(demand)
        self.neighbourhood = neighbourhood
        self.swaps_per_truck = swaps_per_truck
        self.swap_probability = swap_probability
        lower_bounds = []
        upper_bounds = []
        super().__init__(bee_count, abandoned_limit, lower_bounds, upper_bounds, minimization=True)

    def objective_function(self, solutions):
        if solutions.ndim == 3:
            solutions = solutions[np.newaxis, ...]

        obfnc_values = np.empty(len(solutions))
        for sol_num, solution in enumerate(solutions):
            demand_left = self.demand.copy()
            obfnc_value = 0
            for truck_num, truck in enumerate(solution):
                customer_indices = truck[AMOUNT].nonzero()[0]
                truck_dist = 0
                last_customer = -1  # depot
                for index in customer_indices:
                    curr_customer = truck[ORDER, index]
                    demand_left[curr_customer] -= truck[AMOUNT, index]
                    # add distance from last to current customer
                    truck_dist += self.distance[last_customer + 1][curr_customer + 1]
                    last_customer = curr_customer
                # back to depot
                truck_dist += self.distance[last_customer + 1][0]
                obfnc_value += truck_dist * self.transportation_cost[truck_num]
            demand_left_sum = sum(v for v in demand_left if v > 0)
            print(demand_left_sum, demand_left)
            # add demand left to punish unsatisfying solutions but still let the algorithm see
            # an improvement by satisfying more demand
            obfnc_values[sol_num] = obfnc_value + demand_left_sum * 1000
        return obfnc_values

    def random_solutions(self, count):
        sols = np.empty((count, self.truck_count, 2, self.customer_count), dtype=int)
        for sol in range(count):
            for truck in range(self.truck_count):
                sols[sol, truck, AMOUNT] = 0
                sols[sol, truck, ORDER] = np.random.permutation(self.customer_count)
        return sols

    def generate_neighbours(self, solutions):
        new_sols = solutions.copy()
        sums = new_sols[:, :, AMOUNT].sum(axis=2)
        for sol in range(solutions.shape[0]):
            prob_swap = np.random.rand(self.swaps_per_truck * self.truck_count).tolist()
            swap_pos = np.random.randint(self.customer_count, size=self.truck_count * 2 * self.swaps_per_truck + self.truck_count).tolist()
            prob_mutate = np.random.rand(self.truck_count).tolist()
            cust_to_mut = np.random.randint(self.customer_count, size=self.truck_count).tolist()
            for truck in range(self.truck_count):
                for swap in range(self.swaps_per_truck):
                    cur = truck * self.swaps_per_truck + swap
                    if prob_swap[cur] < self.swap_probability:
                        # swap two customer's position
                        new_sols[sol, truck, :, swap_pos[cur]], new_sols[sol, truck, :, swap_pos[cur + 1]] = \
                            new_sols[sol, truck, :, swap_pos[cur + 1]], new_sols[sol, truck, :, swap_pos[cur]]
                # mutate amount delivered for one customer
                if prob_mutate[truck] < 1 - self.swap_probability:
                    new_amount = random.randrange(self.demand[new_sols[sol, truck, ORDER, cust_to_mut[truck]]] + 1)
                    # making sure truck has enough capacity, clipping otherwise
                    new_sum = sums[sol, truck] - new_sols[sol, truck, AMOUNT, cust_to_mut[truck]] + new_amount
                    overflow = new_sum - self.capacity[truck] if new_sum > self.capacity[truck] else 0
                    if (new_amount - overflow) < 0:
                        print("negative")
                    new_sols[sol, truck, AMOUNT, cust_to_mut[truck]] = new_amount - overflow # TODO prevent negative values
        return new_sols, self.max_or_minimizing_objective_function(new_sols)



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
