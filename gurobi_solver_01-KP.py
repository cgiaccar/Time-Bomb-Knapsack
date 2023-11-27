#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:33:11 2023

Contains the solve_deterministic_01KP function used by the exact algorithms

@author: Camilla
"""

import gurobipy as gb


def solve_deterministic_01KP(w, p, c):

    # numbers/data we'll use
    n = len(w)  # number of items

    # optimization model
    knapsack_model = gb.Model()

    # add decision variables
    x = knapsack_model.addVars(n, vtype=gb.GRB.BINARY, name="x")

    # add the constraints
    knapsack_model.addConstr(sum(w[j]*x[j] for j in range(n)) <= c)

    # objective function
    obj_fn = sum(p[j]*x[j] for j in range(n))
    knapsack_model.setObjective(obj_fn, gb.GRB.MAXIMIZE)

    # solve the model and output the solution
    knapsack_model.setParam('OutputFlag', False)
    knapsack_model.optimize()
    return (knapsack_model.x, knapsack_model.objVal)


# FOR TESTING

# simple example to do irl
# w = [8, 5, 10]
# p = [4, 2, 5]
# q = [0.1, 0.9, 0]
# q = [0, 0, 0]

# another example for funsies
w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]
p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]
# q = [0.5, 0, 0.9, 0, 0.2, 0.6, 0.4, 0.3, 0, 1]
c = 77

# w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
# p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
# q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding

# pi = [1-i for i in q]  # probability of NOT exploding
# T = [pi.index(i) for i in pi if i < 1]  # set of time-bomb items (?)
# T = [i for i in range(len(pi)) if pi[i] < 1]

# c = 15  # capacity
n = len(w)  # number of items
# n_T = len(T)  # number of items in T

print(solve_deterministic_01KP(w, p, c))
