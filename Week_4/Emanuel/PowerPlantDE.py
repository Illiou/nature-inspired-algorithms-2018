from Week_4.Emanuel.DifferentialEvolution import DifferentialEvolution
import math


class PowerPlantDE(DifferentialEvolution):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds, plants, markets, purchase_price):
        super().__init__(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds)
        self.plants = plants
        self.markets = markets
        self.purchase_price = purchase_price

    def objective_function(self, solution):
        def production_cost(kwh, kwh_per_plant, cost_per_plant, max_plants):
            if kwh <= 0:
                return 0
            if kwh > kwh_per_plant * max_plants:
                return math.inf
            return math.ceil(kwh / kwh_per_plant) * cost_per_plant

        def demand(price, max_price, max_demand):
            if price > max_price:
                return 0
            if price <= 0:
                return max_demand
            return max_demand - (price**2 * max_demand / max_price**2)

        energy_by_plant = solution[:len(self.plants)]
        energy_by_market = solution[len(self.plants):-len(self.markets)]
        price_by_market = solution[-len(self.markets):]
        purchase_cost = max(sum(energy_by_market) - sum(energy_by_plant), 0) * self.purchase_price
        cost = purchase_cost + sum(production_cost(energy_by_plant[i], *self.plants[i])
                                   for i in range(len(self.plants)))
        revenue = sum(min(energy_by_market[i], demand(price_by_market[i], *self.markets[i])) * price_by_market[i]
                      for i in range(len(self.markets)))
        # negative profit
        return - (revenue - cost)
