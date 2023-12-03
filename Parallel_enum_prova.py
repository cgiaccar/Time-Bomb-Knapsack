"""
First algorithm implementation from the paper:
    Subset enumeration algorithm to solve 01-TimeBomb-Knapsack problems.
Contains some utilities and the TBEnum function described in the paper.

"""

import math
from itertools import chain, combinations
from time import perf_counter
from gurobi_solver_01_KP import solve_deterministic_01KP


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


def task(S, w, c, w_det, p_det, p, pi, z_opt, x_opt, n, T_prime):
    if sum(w[j] for j in S) <= c:  # Discard trivial cases
        (x, d, _) = solve_deterministic_01KP(
            w_det, p_det, c-sum(w[j] for j in S))
        z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

        if z > z_opt:
            z_opt = z  # Update the best solution value
            x_opt = update_x_opt(n, S, x, T_prime)

    return x_opt, z_opt


def TBEnum(w, p, c, q):
    start_time = perf_counter()

    n = len(w)  # number of items
    pi = [1-i for i in q]  # probability of NOT exploding
    T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items
    T_prime = [i for i in range(len(pi)) if pi[i] >= 1]  # deterministic items

    z_opt = 0
    x_opt = [0 for i in range(n)]
    w_det = [w[i] for i in T_prime]  # weight of deterministic items
    p_det = [p[i] for i in T_prime]  # profit of deterministic items

    for S in powerset(T):  # Enumerate all time-bomb item subsets
        x_opt, z_opt = task(S, w, c, w_det, p_det, p,
                            pi, z_opt, x_opt, n, T_prime)

    end_time = perf_counter()
    return (x_opt, z_opt, end_time-start_time)
