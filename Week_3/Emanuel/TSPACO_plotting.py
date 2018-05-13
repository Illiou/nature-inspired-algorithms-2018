import numpy as np
import matplotlib.pyplot as plt
from Week_3.Emanuel.TSPACO import TSPACO
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


if __name__ == '__main__':
    distances_file = "../TSP_Problems/problem_01.tsp"
    initial_pheromone_value = 1
    # evaporation_rate = 0.1
    intensification_value = 1
    iterations = 100
    repetitions = 1

    distance_matrix = np.loadtxt(distances_file)


    num = 5
    lower = 0
    upper = 5

    evaporation_tests = [0.01, 0.05, 0.1, 0.5, 1]
    aco = TSPACO(distance_matrix, initial_pheromone_value, 0, intensification_value, alpha=1, beta=1, ant_number=25)
    alpha_beta_matrix = np.zeros((num, num))
    evaporation_matrix = np.zeros((num,num))
    for a, alpha in enumerate(np.linspace(lower, upper, num)):
        for b, beta in enumerate(np.linspace(lower, upper, num)):
            aco.alpha = alpha
            aco.beta = beta
            for evaporation_rate in evaporation_tests:
                print(f"Calculating for evaporation rate {evaporation_rate}")
                aco.evaporation_rate = evaporation_rate
                best_solution_distances = np.zeros((repetitions, iterations))
                for repetition in range(repetitions):
                    print(f"Repetition {repetition}")
                    aco.initialize()
                    best_solution_distances[repetition] = aco.run(iterations)
                #plt.plot(np.mean(best_solution_distances, axis=0), label=f"Evaporation rate: {evaporation_rate}")
                alpha_beta_matrix[a, b] = np.mean(best_solution_distances)
                evaporation_matrix[a, b] = evaporation_tests[np.argmax()]
                print("Done alpha: {} \t beta: {}".format(alpha, beta))
                print(alpha_beta_matrix)

    # plt.legend()
    # plt.show()
    X, Y = np.meshgrid(np.linspace(lower, upper, num), np.linspace(lower, upper, num))
    print('Shapes:', X.shape, Y.shape, alpha_beta_matrix.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, alpha_beta_matrix, facecolor=cm.inferno)

    ax.set_xlabel('beta')
    ax.set_ylabel('alpha')
    ax.set_zlabel('best solution')

    plt.show()
