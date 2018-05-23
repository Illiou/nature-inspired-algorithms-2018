import numpy as np
from Week_4.Emanuel.PowerPlantDE import PowerPlantDE

# Parameters
population_size = 20
scale_factor = 0.5
crossover_rate = 0.6
lower_bounds = [0, 0, 0, 0, 0, 0, 0, 0, 0]
upper_bounds = [3, 3, 3, 1000, 1000, 1000, 10, 10, 10]

pp_de = PowerPlantDE(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds)

pp_de.run()