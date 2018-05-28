from Week_4.Emanuel.PowerPlantDE import PowerPlantDE
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

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
problems = [problem_1, problem_2, problem_3]
population_sizes = [10, 25, 50, 100, 200]
scale_factors = np.arange(0.4, 1.05, 0.05)
crossover_rates = np.arange(0, 1.1, 0.1)
total_num_of_values = len(population_sizes) * len(scale_factors) * len(crossover_rates)

generations = 500

# Find the best parameters and plot the corresponding run for each problem
for i, problem in enumerate(problems):
    plants = list(zip(problem["k"], problem["c"], problem["m"]))
    markets = list(zip(problem["p"], problem["d"]))
    purchase_price = problem["cost price"]

    best_solutions = np.zeros((total_num_of_values, 4))
    for combi, (population_size, scale_factor, crossover_rate) in enumerate(product(population_sizes, scale_factors, crossover_rates)):

        pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, plants, markets, purchase_price)

        profits = - pp_de.run(generations)
        best_solutions[combi, :] = [profits.max(), population_size, scale_factor, crossover_rate]

    problem_solution = best_solutions[np.argmax(best_solutions[:, 0])]
    population_size = int(problem_solution[1])
    scale_factor = problem_solution[2]
    crossover_rate = problem_solution[3]
    print(population_size, scale_factor, crossover_rate)

    # Run with the best parameters and plot
    pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, plants, markets, purchase_price)
    best_profits = pp_de.run(generations)

    curr_fig, curr_ax = plt.subplots()
    curr_ax.plot(best_profits, label="Best objective function")
    curr_ax.axhline(problem["benchmark"], linestyle="dashed", label="Benchmark")
    curr_ax.set(title="Problem {}".format(i+1), xlabel="Generations", ylabel="Best objective function")
    curr_ax.legend()
    plt.show()
