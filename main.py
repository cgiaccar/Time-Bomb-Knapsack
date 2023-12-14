"""
This files contains some tests for the solvers in the form of different problems.

"""

from gurobi_solver_01_KP import solve_deterministic_01KP
from gekko_solver import solve_with_gekko
from Subset_enumeration_alg import TBEnum
from Parallel_subset_enum_alg import ParTBEnum
import random
import numpy as np


if __name__ == '__main__':

    ### n = 3 ###

    # SOL: x = [0, 0, 1], obj = 5.0
    # w = [8, 5, 10]  # weight
    # p = [4, 2, 5]  # profit
    # q = [0.1, 0.9, 0]  # probability of exploding
    # # q = [0, 0, 0]  # all zeros --> standard knapsack
    # c = 15

    ### n = 8 ###

    # SOL: x = [1, 1, 1, 0, 0, 0, 1, 0], obj = 28.0
    # w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
    # p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
    # q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
    # # q = [0, 0, 0, 0, 0, 0, 0, 0]  # all zeros --> standard knapsack
    # c = 15  # capacity

    ### n = 10 ###

    # SOL: x = [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], obj = 45.2
    # w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]  # weight
    # p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]  # profit
    # q = [0.5, 0, 0.9, 0, 0.2, 0.6, 0.4, 0.3, 0, 1]  # probability of exploding
    # # q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # all zeros --> standard knapsack
    # c = 77

    ### random examples ###

    np.random.seed(0)
    random.seed(0)

    # SOL for n=20, frac=4 : x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], obj = 415.4399392044384
    # SOL for n=21, frac=4 : x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], obj = 313.24171416014656
    n = 21
    frac = 4

    q = np.random.uniform(0, 0.99999, n)
    p = np.random.randint(1, 300, n)

    # needs to be a list to avoid NoneType errors later on
    w = [random.randint(1, 300) for i in range(n)]

    c = int(sum(w)/frac)

    print(f"{w = }\n{p = }\n{c = }\n{q = }")

    # Print solutions:

    gurobi_x, gurobi_obj, gurobi_time = solve_deterministic_01KP(w, p, c)
    print(
        f"\nSimple Gurobi solution:\nx = {gurobi_x} \nobj = {gurobi_obj} \ntime = {gurobi_time:0.6f}")

    gekko_x, gekko_obj, gekko_time = solve_with_gekko(w, p, c, q)
    print(
        f"\nGEKKO solution:\nx = {gekko_x} \nobj = {gekko_obj} \ntime = {gekko_time:0.6f}")

    enum_x, enum_obj, enum_time = TBEnum(w, p, c, q)
    print(
        f"\nSubset Enumeration algorithm solution:\nx = {enum_x} \nobj = {enum_obj} \ntime = {enum_time:0.6f}")

    par_x, par_obj, par_time = ParTBEnum(w, p, c, q)
    print(
        f"\nParallel Subset Enumeration algorithm solution:\nx = {par_x} \nobj = {par_obj} \ntime = {par_time:0.6f}")
