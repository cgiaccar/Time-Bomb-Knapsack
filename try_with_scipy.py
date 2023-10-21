#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:49:57 2023

@author: Camilla
"""

import numpy as np
from scipy import optimize
from scipy.optimize import milp

w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
pi = [1-i for i in q]  # probability of NOT exploding
c = 15  # capacity
n = len(w)  # number of items

T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items

sizes = np.array([21, 11, 15, 9, 34, 25, 41, 52])
values = np.array([22, 12, 16, 10, 35, 26, 42, 53])
bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
integrality = np.full_like(values, True)  # x_i are integers
capacity = 100
constraints = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)
res = milp(c=-values, constraints=constraints,
           integrality=integrality, bounds=bounds)

print(res.success)  # -> True
print(res.x)    # -> array([1., 1., 0., 1., 1., 1., 0., 0.])
