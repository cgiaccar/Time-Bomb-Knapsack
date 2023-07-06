#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:29:47 2023

@author: Camilla
"""

import gurobipy as gb


def solve_ILP_formulation(w, p, c):

    # numbers/data we'll use
    n = len(w)  # number of items

    # optimization model
    knapsack_model = gb.Model()

    # add decision variables
    x = knapsack_model.addVars(n, vtype=gb.GRB.BINARY, name="x")
    z = knapsack_model.addVars(n, n, vtype=gb.GRB.BINARY, name="z")

    # add the constraints
    knapsack_model.addConstr(sum(w[j]*x[j] for j in range(n)) <= c)
    knapsack_model.addConstrs(
        z[j, k] >= x[j]+x[k]-1 for j in range(n) for k in range(n))

    # objective function
    obj_fn = sum(p[j]*x[j] for j in range(n)) - \
        sum(sum(p[j]*q[k]*z[j, k] for k in range(n)) for j in range(n))
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

print(solve_ILP_formulation(w, p, c))


# To be put in the B&B file so that we have S?
# Right now it's just to have notes

# second_lower_bound = sum(p[j] for j in sol_ILP_formulation) * \
#     math.prod(pi[j] for j in sol_ILP_formulation)

# second_upper_bound = ? they seem to be using another alg from someone else
# Finally, for the continuous relaxation upper bound 𝑧̄2, we observe that
# branching conditions can be easily handled by simply adding these constraints
# to the definition of the feasible set 𝑃. As a consequence, the initial
# solution consists of the items in 𝑆. In addition, at each iteration, the
# improving direction 𝑦̄ to be determined must satisfy branching conditions(26)
# as well, i.e., time-bomb items in 𝑆 and 𝑆̄ are fixed a-priori to 1 and to 0,
# respectively, when solving the continuous relaxation of the deterministic
# knapsack problem required by(15).
