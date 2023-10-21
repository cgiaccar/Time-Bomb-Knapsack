#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 19:44:17 2023

This doesn't actually work, since Gurobi is able to solve problems with
at most 2 variables multiplying and this problem has the prod_alpha element in
the objective function. When running, it gives error
    GurobiError: Invalid argument to QuadExpr multiplication
from line 44.
This file can still be useful as a reference when implementing this model at
the end with another commercial solver

@author: Camilla
"""

import gurobipy as gb
import math


# numbers/data we'll use

w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding

pi = [1-i for i in q]  # probability of NOT exploding
T = [pi.index(i) for i in pi if i < 1]  # set of time-bomb items (?)

c = 15  # capacity
n = len(w)  # number of items
n_T = len(T)  # number of items in T


# optimization model
knapsack_model = gb.Model()

# add decision variables
x = knapsack_model.addVars(n, vtype=gb.GRB.BINARY, name="x")
alpha = knapsack_model.addVars(n_T, vtype=gb.GRB.INTEGER, name="alpha")  # (?)
prod_alpha = knapsack_model.addVar(vtype=gb.GRB.CONTINUOUS, name="prod_alpha")

# add the constraints
knapsack_model.addConstr(sum(w[j]*x[j] for j in range(n)) <= c)
knapsack_model.addConstrs(alpha[j] == 1-q[j]*x[j] for j in range(n_T))  # (?)
# this next constraint doesn't work
knapsack_model.addConstr(prod_alpha == math.prod(alpha[j] for j in range(n_T)))

# objective function
obj_fn = sum(p[j]*x[j] for j in range(n))*prod_alpha
knapsack_model.setObjective(obj_fn, gb.GRB.MAXIMIZE)

# solve the model and output the solution
knapsack_model.setParam('OutputFlag', False)
knapsack_model.optimize()
print('Optimization is done. Objective function Value: %.2f' %
      knapsack_model.objVal)
for v in knapsack_model.getVars():
    print('%s: %g' % (v.varName, v.x))
