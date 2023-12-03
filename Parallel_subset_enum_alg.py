"""
First algorithm implementation from the paper:
    Subset enumeration algorithm to solve 01-TimeBomb-Knapsack problems.
Contains some utilities and the TBEnum function described in the paper.

"""

from itertools import repeat
import multiprocessing as mp
import math
from itertools import chain, combinations
from time import perf_counter
from gurobi_solver_01_KP import solve_deterministic_01KP
import time


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def update_x_opt(n, S, x, T_prime):
    x_opt = [0 for i in range(n)]
    for index in S:
        x_opt[index] = 1
    i = 0
    for index in T_prime:
        if x[i] == 1:
            x_opt[index] = 1
        i += 1
    return x_opt


def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]


def wrapper(tup):
    return work_log(*tup)


def work_log(sets, tup):
    w = tup[0]
    p = tup[1]
    c = tup[2]
    q = tup[3]

    n = len(w)  # number of items
    pi = [1-i for i in q]  # probability of NOT exploding
    T_prime = [i for i in range(len(pi)) if pi[i] >= 1]  # deterministic items

    z_opt = 0
    x_opt = [0 for i in range(n)]
    w_det = [w[i] for i in T_prime]  # weight of deterministic items
    p_det = [p[i] for i in T_prime]  # profit of deterministic items

    for S in sets:  # Enumerate all time-bomb item subsets
        if sum(w[j] for j in S) <= c:  # Discard trivial cases
            (x, d, _) = solve_deterministic_01KP(
                w_det, p_det, c-sum(w[j] for j in S))
            z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

            if z > z_opt:
                z_opt = z  # Update the best solution value
                x_opt = update_x_opt(n, S, x, T_prime)
                return x_opt, z_opt


def ParTBEnum(w, p, c, q):
    start_time = perf_counter()

    print("hello")

    # n = len(w)  # number of items
    pi = [1-i for i in q]  # probability of NOT exploding
    T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items
    # T_prime = [i for i in range(len(pi)) if pi[i] >= 1]  # deterministic items

    # z_opt = 0
    # x_opt = [0 for i in range(n)]
    # w_det = [w[i] for i in T_prime]  # weight of deterministic items
    # p_det = [p[i] for i in T_prime]  # profit of deterministic items

    pwset = powerset(T)
    # divide powerset into chunks
    sets = list(chunks([*pwset], mp.cpu_count()))

    # pool.map() wants a single tuple as argument
    # tup = [w, c, w_det, p_det, pi, z_opt, x_opt]
    tup = [w, p, c, q]
    # arg2 = [w, p, c, q]*len(sets)
    # tup = [*zip(sets, arg2)]

    pool = mp.Pool(mp.cpu_count())  # pool setup
    result = pool.starmap(work_log, zip(sets, repeat(tup)))
    # kwds={'w': w, 'c': c, 'w_det': w_det, 'p_det': p_det, 'pi': pi, 'z_opt': z_opt, 'x_opt': x_opt})  # parallel execution
    print(result)

    end_time = perf_counter()
    # return (x_opt, z_opt, end_time-start_time)


if __name__ == '__main__':
    # another example
    w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]  # weight
    p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]  # profit
    q = [0.5, 0, 0.9, 0, 0.2, 0.6, 0.4, 0.3, 0, 1]  # probability of exploding
    # q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # all zeros --> standard knapsack
    c = 77

    print("Number of cpu : ", mp.cpu_count())

    ParTBEnum(w, p, c, q)
