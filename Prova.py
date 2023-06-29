#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 17:55:07 2023

@author: Camilla
"""

# 1 - Import gurobi package
import gurobipy as gb

print("Hello, this is a basic Knapsack example :D\n")

# 2 - creating the data (weights, values and capacity)
w = [4, 2, 5, 4, 5, 1, 3, 5]
v = [10, 5, 18, 12, 15, 1, 2, 8]
C = 15
N = len(w)

# 3 - create an optimization model
knapsack_model = gb.Model()

# 4 - add decision variables
x = knapsack_model.addVars(N, vtype=gb.GRB.BINARY, name="x")

# 5 - define the objective function
obj_fn = sum(v[i]*x[i] for i in range(N))
knapsack_model.setObjective(obj_fn, gb.GRB.MAXIMIZE)

# 6 - add the constraints
knapsack_model.addConstr(sum(w[i]*x[i] for i in range(N)) <= C)

# 7 - solve the model and output the solution
knapsack_model.setParam('OutputFlag', False)
knapsack_model.optimize()
print('Optimization is done. Objective function Value: %.2f' %
      knapsack_model.objVal)
for v in knapsack_model.getVars():
    print('%s: %g' % (v.varName, v.x))
