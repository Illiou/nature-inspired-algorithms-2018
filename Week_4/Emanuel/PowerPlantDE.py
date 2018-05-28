from Week_4.Emanuel.DifferentialEvolution import DifferentialEvolution
import numpy as np
import math


class PowerPlantDE(DifferentialEvolution):
    def __init__(self, population_size, scale_factor, crossover_rate, plants, markets, purchase_price,
                 lower_bounds=None, upper_bounds=None):
        self.plants = plants
        self.markets = markets
        self.purchase_price = purchase_price
        if lower_bounds is None:
            lower_bounds = [0] * (len(self.plants) + len(self.markets) * 2)
        if upper_bounds is None:
            energy_upper = min(p[0] * p[2] for p in self.plants) # min produced max kwh of all plants
            sold_upper = max(m[1] for m in self.markets) # max demand of all markets
            price_upper = max(m[0] for m in self.markets) # max price at which customers buy of all markets
            upper_bounds = ([energy_upper] * len(self.plants) +
                            [sold_upper] * len(self.markets) +
                            [price_upper] * len(self.markets))
        super().__init__(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds)

    def objective_function(self, solution):
        def cost_per_plant(kwh, kwh_per_plant, cost_per_plant, max_plants):
            res = np.ceil(kwh / kwh_per_plant) * cost_per_plant
            res[kwh > kwh_per_plant * max_plants] = math.inf
            res[kwh <= 0] = 0
            return res

        def demand_per_plant(price, max_price, max_demand):
            res = max_demand - (price**2 * max_demand / max_price**2)
            res[price <= 0] = max_demand
            res[price > max_price] = 0
            return res

        # to make slices below work in one-dimensional case
        if len(solution.shape) == 1:
            solution = solution[np.newaxis]

        energy_by_plant = solution[:, :len(self.plants)]
        energy_by_market = solution[:, len(self.plants):-len(self.markets)]
        price_by_market = solution[:, -len(self.markets):]

        purchase_cost = np.maximum(np.sum(energy_by_market, axis=1) - np.sum(energy_by_plant, axis=1), 0)\
                        * self.purchase_price
        production_cost = np.zeros(energy_by_plant.shape[0])
        for i in range(len(self.plants)):
            production_cost += cost_per_plant(energy_by_plant[:, i], *self.plants[i])
        cost = purchase_cost + production_cost
        revenue = np.zeros(energy_by_market.shape[0])
        for i in range(len(self.markets)):
            revenue += np.minimum(energy_by_market[:, i],
                               demand_per_plant(price_by_market[:, i], *self.markets[i]))\
                    * price_by_market[:, i]
        # negative profit
        return - (revenue - cost)
