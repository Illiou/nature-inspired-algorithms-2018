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

# Parameters
problem_num = 1
problem = problems[problem_num]
population_size = 50
scale_factor = 0.5
crossover_rate = 0.6
generations = 1000
repetitions = 50

plants = list(zip(problem["k"], problem["c"], problem["m"]))
markets = list(zip(problem["p"], problem["d"]))
purchase_price = problem["cost price"]

pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, plants, markets, purchase_price)


tests = {"population_size": [10, 30, 50, 100, 200],
         "scale_factor": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
         "crossover_rate": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}

figures = []

for test_name, test_values in tests.items():
    curr_fig, curr_ax = plt.subplots()
    figures.append(curr_fig)
    value_before_test = getattr(pp_de, test_name)
    for test_value in test_values:
        print(f"Calculating for {test_name}: {test_value}")
        setattr(pp_de, test_name, test_value)
        best_profits = np.zeros((repetitions, generations))
        for repetition in range(repetitions):
            print(f"Repetition {repetition}")
            pp_de.initialize()
            best_profits[repetition] = pp_de.run(generations)
        curr_ax.plot(best_profits.mean(axis=0), label=f"{test_name.capitalize().replace('_', ' ')}: {test_value}")
    setattr(pp_de, test_name, value_before_test)
    curr_ax.axhline(problem["benchmark"], linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_num}", xlabel="Generations", ylabel="Profit of best solution")
    curr_ax.legend()

for fig in figures:
    fig.show()

