import numpy as np
import matplotlib.pyplot as plt


def initialize(pop_size, bounds, max_gen=1):
    # Integer oder continuous values?
    return np.array([np.random.randint(bounds[0, i], bounds[1, i], pop_size) for i in range(len(bounds[0]))]).T


def generate_donor():
    return None


def generate_trial():
    return None


def fitness(pop):
    return np.zeros(pop.shape)


if __name__ == '__main__':
    # Parameters
    scale_factor_F = 0.5
    crossover_rate = 0.6
    population_size = 20
    # Convergence criteria
    max_generation = 500
    epsilon = 0.001
    # Define problem
    boundaries = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 1000, 1000, 1000, 10, 10, 10]])
    # Initialize
    population = initialize(population_size, boundaries)
    population_fitness = fitness(population)
    generation = 0
    change = 42

    while generation < max_generation and change > epsilon:
        for i, individual in enumerate(population):
            donor = generate_donor(i)
            trial = generate_trial()
            trial_fitness = fitness([trial])[0]
            if trial_fitness <= population_fitness[i]:
                population[i] = trial
                population_fitness[i] = trial_fitness
        generation += 1
