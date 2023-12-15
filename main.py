"""
This files contains a comparison of the solvers in the form of different random problems and a final plot.

"""

# from gurobi_solver_01_KP import solve_deterministic_01KP
from gekko_solver import solve_with_gekko
from Subset_enumeration_alg import TBEnum
from Parallel_subset_enum_alg import ParTBEnum
import matplotlib.pyplot as plt
import numpy as np
import random


if __name__ == '__main__':

    np.random.seed(0)
    random.seed(0)

    frac = 4

    # create time lists for plot
    y_gekko = []
    y_enum = []
    y_par = []

    for n in range(1, 20):

        ### Random problem ###
        q = np.random.uniform(0, 0.99999, n)
        p = np.random.randint(1, 300, n)
        # w needs to be a list to avoid NoneType errors later on
        w = [random.randint(1, 300) for i in range(n)]
        c = int(sum(w)/frac)

        print(f"{w = }\n{p = }\n{c = }\n{q = }")

        ### Print solutions ###

        # gurobi_x, gurobi_obj, gurobi_time = solve_deterministic_01KP(w, p, c)
        # print(
        #     f"\nSimple Gurobi solution:\nx = {gurobi_x} \nobj = {gurobi_obj} \ntime = {gurobi_time:0.6f}")

        gekko_x, gekko_obj, gekko_time = solve_with_gekko(w, p, c, q)
        print(
            f"\nGEKKO solution:\nx = {gekko_x} \nobj = {gekko_obj} \ntime = {gekko_time:0.6f}")

        enum_x, enum_obj, enum_time = TBEnum(w, p, c, q)
        print(
            f"\nSubset Enumeration algorithm solution:\nx = {enum_x} \nobj = {enum_obj} \ntime = {enum_time:0.6f}")

        par_x, par_obj, par_time = ParTBEnum(w, p, c, q)
        print(
            f"\nParallel Subset Enumeration algorithm solution:\nx = {par_x} \nobj = {par_obj} \ntime = {par_time:0.6f}")

        # save execution time
        y_gekko.append(gekko_time)
        y_enum.append(enum_time)
        y_par.append(par_time)

    ### Plot results ###
    x = range(1, 20)

    plt.plot(x, y_gekko, label='gekko')
    plt.plot(x, y_enum, label='enum')
    plt.plot(x, y_par, label='parEnum')

    plt.xlabel("Number of elements")
    plt.ylabel("Execution time")
    plt.legend()
    plt.title('Time Comparison')
    plt.show()
