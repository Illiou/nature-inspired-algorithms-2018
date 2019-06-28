from Final.ArtificialBeeAlgorithm import ArtificialBeeColony
import numpy as np
import math
import matplotlib.pyplot as plt
from Week_4.Emanuel.PowerPlantDE_test_3 import problems


class PowerPlantABC(ArtificialBeeColony):
    def __init__(self, bee_count, abandoned_limit, plants, markets, purchase_price,
                 lower_bounds=None, upper_bounds=None):
        self.plants = plants
        self.markets = markets
        self.purchase_price = purchase_price
        if lower_bounds is None:
            lower_bounds = [0] * (len(self.plants) + len(self.markets) * 2)
        if upper_bounds is None:
            energy_upper = min(p[0] * p[2] for p in self.plants)  # min produced max kwh of all plants
            sold_upper = max(m[1] for m in self.markets)  # max demand of all markets
            price_upper = max(m[0] for m in self.markets)  # max price at which customers buy of all markets
            upper_bounds = ([energy_upper] * len(self.plants) +
                            [sold_upper] * len(self.markets) +
                            [price_upper] * len(self.markets))
        super().__init__(bee_count, abandoned_limit, lower_bounds, upper_bounds, True)

    def objective_function(self, solutions):
        def cost_per_plant(kwh, kwh_per_plant, cost_per_plant, max_plants):
            res = np.ceil(kwh / kwh_per_plant) * cost_per_plant
            res[kwh > kwh_per_plant * max_plants] = math.inf
            res[kwh <= 0] = 0
            return res

        def demand_per_plant(price, max_price, max_demand):
            res = max_demand - (price ** 2 * max_demand / max_price ** 2)
            res[price <= 0] = max_demand
            res[price > max_price] = 0
            return res

        if solutions.ndim == 1:
            solutions = solutions[np.newaxis, ...]

        energy_by_plant = solutions[:, :len(self.plants)]
        energy_by_market = solutions[:, len(self.plants):-len(self.markets)]
        price_by_market = solutions[:, -len(self.markets):]

        purchase_cost = np.maximum(np.sum(energy_by_market, axis=1) - np.sum(energy_by_plant, axis=1), 0) \
                        * self.purchase_price
        production_cost = np.zeros(energy_by_plant.shape[0])
        for i in range(len(self.plants)):
            production_cost += cost_per_plant(energy_by_plant[:, i], *self.plants[i])
        cost = purchase_cost + production_cost
        revenue = np.zeros(energy_by_market.shape[0])
        for i in range(len(self.markets)):
            revenue += np.minimum(energy_by_market[:, i],
                                  demand_per_plant(price_by_market[:, i], *self.markets[i])) \
                       * price_by_market[:, i]
        # for minimization
        return -(revenue - cost)

    def run(self, iterations=100):
        result = super().run(iterations)
        return -result[0], result[1]


if __name__ == '__main__':
    problem_num = 3
    problem = problems[problem_num]
    bee_count = 70
    iterations = 10000
    limit = 100

    plants = list(zip(problem["k"], problem["c"], problem["m"]))
    markets = list(zip(problem["p"], problem["d"]))
    purchase_price = problem["cost price"]
    benchmark = problem["benchmark"]
    best_nectar, best_solution = PowerPlantABC(bee_count, limit, plants, markets, purchase_price).run(iterations)
    print(best_nectar)
    print(best_solution)

    curr_fig, curr_ax = plt.subplots()
    curr_ax.plot(best_nectar, label="Best nectar")
    curr_ax.axhline(benchmark, linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_num}", xlabel="iteration", ylabel="Best objective function")
    curr_ax.legend()
    plt.show()
