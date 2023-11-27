#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:03:32 2023

@author: Camilla
"""

import gurobipy as gb


def solve_first_upper_bound(w, p, c):

    # numbers/data we'll use
    n = len(w)  # number of items

    # optimization model
    knapsack_model = gb.Model()

    # add decision variables
    x = knapsack_model.addVars(n, vtype=gb.GRB.BINARY, name="x")

    # add the constraints
    knapsack_model.addConstr(sum(w[j]*x[j] for j in range(n)) <= c)

    # objective function
    obj_fn = sum(p[j]*pi[j]*x[j] for j in range(n))
    knapsack_model.setObjective(obj_fn, gb.GRB.MAXIMIZE)

    # solve the model and output the solution
    knapsack_model.setParam('OutputFlag', False)
    knapsack_model.optimize()
    return knapsack_model.objVal


# FOR TESTING
w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding

pi = [1-i for i in q]  # probability of NOT exploding
T = [pi.index(i) for i in pi if i < 1]  # set of time-bomb items (?)

c = 15  # capacity
n = len(w)  # number of items
n_T = len(T)  # number of items in T

print(solve_first_upper_bound(w, p, c))


# To be put in the B&B file so that we have S?
# Right now it's just to have notes

# w_new = time-bomb items in set F and deterministic items
# p_new = time-bomb items in set F and deterministic items
# c_S = c - sum(w[j] for j in S)
# p_S = sum(p[j] for j in S)
# q_S = math.prod(1-q[j] for j in S)
# first_upper_bound_F = solve_first_upper_bound(w_new, p_new, c_S)
# first_upper_bound = (p_S + first_upper_bound_F) * q_S

# first_lower_bound = sum(p[j] for j in sol_first_upper_bound) * \
#     math.prod(pi[j] for j in sol_first_upper_bound)
