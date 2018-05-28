from Week_4.Emanuel.PowerPlantDE import PowerPlantDE
import matplotlib.pyplot as plt
import numpy as np

problems = [{}, # placeholder for 0
            {"c": [10000, 80000, 400000],
             "p": [0.45, 0.25, 0.2],
             "d": [2000000, 30000000, 20000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.6,
             "benchmark": 1514312},

            {"c": [10000, 80000, 400000],
             "p": [0.45, 0.25, 0.2],
             "d": [2000000, 30000000, 20000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.1,
             "benchmark": 1818406},

            {"c": [10000, 80000, 400000],
             "p": [0.5, 0.3, 0.1],
             "d": [1000000, 5000000, 5000000],
             "k": [50000, 600000, 4000000],
             "m": [100, 50, 3],
             "cost price": 0.6,
             "benchmark": 404041}]

if __name__ == '__main__':
    # Parameters
    problem_num = 1
    problem = problems[problem_num]
    population_size = 50
    scale_factor = 0.5
    crossover_rate = 0.7

    plants = list(zip(problem["k"], problem["c"], problem["m"]))
    markets = list(zip(problem["p"], problem["d"]))
    purchase_price = problem["cost price"]

    generations = 3000
    iterations = 100

    all_best_profits = np.empty([iterations, generations])
    benchmark_reached = 0
    for iteration in range(iterations):
        pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, plants, markets, purchase_price)
        profits = pp_de.run(generations)
        if profits[-1] >= problem["benchmark"]:
            benchmark_reached += 1
        all_best_profits[iteration] = profits
    best_profits = np.mean(all_best_profits, axis=0)
    print("best are {}".format(all_best_profits[:, -1]))
    print("benchmark reached {} of {} times".format(benchmark_reached, iterations))

    curr_fig, curr_ax = plt.subplots()
    curr_ax.plot(best_profits, label="Best objective function")
    curr_ax.axhline(problem["benchmark"], linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_num}", xlabel="Generations", ylabel="Best objective function")
    curr_ax.legend()
    # curr_fig.show()
    plt.show()
