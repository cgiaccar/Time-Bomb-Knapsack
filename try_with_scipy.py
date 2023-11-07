#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:49:57 2023

@author: Camilla
"""

###################### SIMPLE KNAPSACK ##########################

import numpy as np
from scipy import optimize
from scipy.optimize import milp

w = np.array([4, 2, 5, 4, 5, 1, 3, 5])  # weight
p = np.array([10, 5, 18, 12, 15, 1, 2, 8])  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
pi = [1-i for i in q]  # probability of NOT exploding
c = 15  # capacity
n = len(w)  # number of items

T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items

bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
integrality = np.full_like(p, True)  # x_i are integers
constraints = optimize.LinearConstraint(A=w, lb=0, ub=c)
res = milp(c=-p, constraints=constraints,
           integrality=integrality, bounds=bounds)

print(res.success)   # print if resolution is successful
print(res.fun)       # print value of objective fz
print(res.x)         # print value of x variables

######################################################################
