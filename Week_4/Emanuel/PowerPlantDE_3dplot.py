from Week_4.Emanuel.PowerPlantDE import PowerPlantDE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
generations = 500
repetitions = 10

scale_upper, scale_lower, scale_num = 0.3, 1, 15
crossover_upper, crossover_lower, crossover_num = 0, 1, 21

scale_factors = np.linspace(scale_upper, scale_lower, scale_num)
crossover_rates = np.linspace(crossover_upper, crossover_lower, crossover_num)

plants = list(zip(problem["k"], problem["c"], problem["m"]))
markets = list(zip(problem["p"], problem["d"]))
purchase_price = problem["cost price"]

pp_de = PowerPlantDE(population_size, 0, 0, plants, markets, purchase_price)


result_matrix = np.zeros((repetitions, crossover_num, scale_num))
for i in range(repetitions):
    print(f"Calculation repetition {i}")
    for x, scale_factor in enumerate(scale_factors):
        print(f"x: {x}")
        for y, crossover_rate in enumerate(crossover_rates):
            pp_de.scale_factor = scale_factor
            pp_de.crossover_rate = crossover_rate
            pp_de.initialize()
            result_matrix[i, y, x] = pp_de.run(generations).max()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y = np.meshgrid(scale_factors, crossover_rates)
ax.plot_surface(x, y, result_matrix.mean(axis=0))

ax.set(title=f"Problem {problem_num}", xlabel="Scale factor", ylabel="Crossover rate", zlabel="Profit of best solution")

fig.show()
