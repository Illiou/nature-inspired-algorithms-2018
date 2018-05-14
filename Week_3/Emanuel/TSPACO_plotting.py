import numpy as np
import matplotlib.pyplot as plt
from TSPACO import TSPACO
from matplotlib import cm

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from matplotlib import cbook
from matplotlib.colors import LightSource


if __name__ == '__main__':
    # loading problem
    problem = 1
    distances_file = f"../TSP_Problems/problem_0{problem}.tsp"
    distance_matrix = np.loadtxt(distances_file)

    # default values
    initialization_value = 1
    evaporation_rate = 0.05
    intensification_value = 1
    iterations = 10
    repetitions = 1
    alpha = 1
    beta = 1
    ant_number = 30
    n_best_to_intensify = 1

    aco = TSPACO(distance_matrix, initialization_value, evaporation_rate, intensification_value,
                 alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)

    num = 10
    lower = 0
    upper = 5

    evaporation_tests = [0.01, 0.05, 0.1, 0.5, 1]
    alpha_beta_matrix = np.zeros((num, num))
    evaporation_matrix = np.zeros((num,num))
    for a, alpha in enumerate(np.linspace(lower, upper, num)):
        for b, beta in enumerate(np.linspace(lower, upper, num)):
            aco.alpha = alpha
            aco.beta = beta
            evaporation_results = np.zeros(len(evaporation_tests))
            for index, evaporation_rate in enumerate(evaporation_tests):
                print(f"Calculating for evaporation rate {evaporation_rate}")
                aco.evaporation_rate = evaporation_rate
                aco.initialize()
                evaporation_results[index] = aco.run(iterations)[-1]
                # best_solution_distances = np.zeros((repetitions, iterations))
                # for repetition in range(repetitions):
                #     print(f"Repetition {repetition}")
                #     aco.initialize()
                #     best_solution_distances[repetition] = aco.run(iterations)
                #plt.plot(np.mean(best_solution_distances, axis=0), label=f"Evaporation rate: {evaporation_rate}")

            alpha_beta_matrix[a, b] = np.min(evaporation_results)
            evaporation_matrix[a, b] = evaporation_tests[np.argmin(evaporation_results)]
            print("Done alpha: {} \t beta: {}".format(alpha, beta))
            print(alpha_beta_matrix)
            print("Evaporation Matrix:")
            print(evaporation_matrix)

    np.savetxt("alpha_beta_matrix.csv", alpha_beta_matrix, delimiter=",")
    np.savetxt("evaporation_matrix.csv", evaporation_matrix, delimiter=",")

    # plt.legend()
    # plt.show()
    X, Y = np.meshgrid(np.linspace(lower, upper, num), np.linspace(lower, upper, num))
    print('Shapes:', X.shape, Y.shape, alpha_beta_matrix.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # norm = matplotlib.colors.Normalize(vmin=.0, vmax=1.)
    # ax.plot_surface(X, Y, alpha_beta_matrix, facecolor=cm.inferno, shade=False)

    #ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    #rgb = ls.shade(evaporation_matrix, cmap=cm.bone, vert_exag=0.1, blend_mode='soft', vmin=0., vmax =0.1)
    #surf = ax.plot_surface(X, Y, alpha_beta_matrix, rstride=1, cstride=1, facecolors=rgb,
    #                       linewidth=0, antialiased=False, shade=False, vmin=0., vmax =0.01)


    ax.plot_surface(X, Y, alpha_beta_matrix, facecolors=cm.inferno(evaporation_matrix))
    m = cm.ScalarMappable(cmap=cm.inferno)
    m.set_array(evaporation_matrix)
    plt.colorbar(m)

    ax.set_xlabel('beta')
    ax.set_ylabel('alpha')
    ax.set_zlabel('best solution')

    plt.show()
