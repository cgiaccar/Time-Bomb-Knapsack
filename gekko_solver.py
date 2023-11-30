"""
GEKKO solver for 01-TimeBomb-Knapsack problems.
Contains the solve_with_gekko function called in the main.

"""

import numpy as np
from gekko import GEKKO


def solve_with_gekko(w, p, c, q):

    n = len(w)  # number of items
    pi = [1-i for i in q]  # probability of NOT exploding
    T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items

    m = GEKKO(remote=False)  # create GEKKO model

    # variables
    x = [m.Var(lb=0, ub=1, integer=True) for j in range(n)]

    # constraint
    m.Equations([sum(w[j]*x[j] for j in range(n)) <= c])

    # objective function
    m.Maximize(sum(p[i]*x[i] for i in range(n)) *
               np.prod([1-(q[j]*x[j]) for j in T]))

    m.solve(disp=False)

    return ([item for items in x for item in items], -m.options.OBJFCNVAL, m.options.SOLVETIME)
