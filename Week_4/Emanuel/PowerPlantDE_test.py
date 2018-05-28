from Week_4.Emanuel.PowerPlantDE import PowerPlantDE
import matplotlib.pyplot as plt
import numpy as np

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
population_size = 50
scale_factor = 0.5
crossover_rate = 0.6
lower_bounds = [0, 0, 0, 0, 0, 0, 0, 0, 0]
energy_up = min(problem["k"][i] * problem["m"][i] for i in range(len(problem["k"])))
sold_up = max(problem["d"])
price_up = max(problem["p"])
upper_bounds = [energy_up, energy_up, energy_up, sold_up, sold_up, sold_up, price_up, price_up, price_up]
plants = list(zip(problem["k"], problem["c"], problem["m"]))
markets = list(zip(problem["p"], problem["d"]))
purchase_price = problem["cost price"]

pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds,
                     plants, markets, purchase_price)

generations = 500

best_profits = - pp_de.run(generations)

curr_fig, curr_ax = plt.subplots()
curr_ax.plot(best_profits, label="Best objective function")
curr_ax.axhline(problem["benchmark"], linestyle="dashed", label="Benchmark")
curr_ax.set(title="Problem 1", xlabel="Generations", ylabel="Best objective function")
curr_ax.legend()
curr_fig.show()
