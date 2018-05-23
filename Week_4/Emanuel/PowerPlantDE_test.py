import numpy as np
from Week_4.Emanuel.PowerPlantDE import PowerPlantDE

problem_1 = {"c": [10000, 80000, 400000],
             "p": [0.45, 0.25, 0.2],
             "d": [2000000, 30000000, 20000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.6,
             "benchmark": 1514312}

problem_2 = {"c": [10000, 80000, 400000],
             "p": [0.45, 0.25, 0.2],
             "d": [2000000, 30000000, 20000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.1,
             "benchmark": 1818406}

problem_3 = {"c": [10000, 80000, 400000],
             "p": [0.5, 0.3, 0.1],
             "d": [1000000, 5000000, 5000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.6,
             "benchmark": 404041}

# Parameters
problem = problem_1
population_size = 20
scale_factor = 0.5
crossover_rate = 0.6
lower_bounds = [0, 0, 0, 0, 0, 0, 0, 0, 0]
upper_bounds = [3, 3, 3, 1000, 1000, 1000, 10, 10, 10]
plants = list(zip(problem["k"], problem["c"], problem["m"]))
markets = list(zip(problem["p"], problem["d"]))
purchase_price = problem["cost price"]

pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds, plants, markets, purchase_price)

pp_de.run(10)
