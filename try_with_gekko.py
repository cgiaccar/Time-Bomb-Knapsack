#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 19:16:22 2023

@author: Camilla
"""

# from gekko import GEKKO
# m = GEKKO(remote=False)  # create GEKKO model
# x = m.Var()            # define new variable, default=0
# y = m.Var()            # define new variable, default=0
# m.Equations([3*x+2*y == 1, x+2*y == 0])  # equations
# m.solve(disp=False)    # solve
# print(x.value, y.value)  # print solution


import random

import numpy as np
from gekko import GEKKO
np.random.seed(0)
random.seed(0)

N = 10
frac = 2
T = np.random.choice(range(N), N//frac)

print(T)

q = np.random.uniform(0, 0.99999, size=N)  # il prof aveva scritto size=len(T)
q /= q.sum()
p = np.random.uniform(0, 10, size=N)

w = np.random.uniform(0, 0.99999, size=N)
c = w.sum()/4


m = GEKKO(remote=False)

x = [m.Var(lb=0, ub=1, integer=True) for i in range(N)]

# m.Equation(==Demand)
m.Obj(-(m.sum([p[j]*x[j] for j in range(N)]))
      * (np.prod([1 - q[i]*x[i] for i in T])))
m.options.SOLVER = 1

m.solve()
print(x)


# https://www.gurobi.com/documentation/current/refman/py_model_agc_poly.html

# import numpy as np
# from gekko import GEKKO

# N = 10
# T = [0, 1, 2, 3, 4]

# q = np.random.uniform(0, 0.99999, size=len(T))
# q /= q.sum()
# p = np.random.uniform(0, 10, size=N)

# w = np.random.uniform(0, 0.99999, size=N)
# c = w.sum()/4


# m = GEKKO(remote=False)

# x = [m.Var(lb=0, ub=1, integer=True) for i in range(N)]

# # m.Equation(==Demand)
# m.Obj(-(m.sum([p[j]*x[j] for j in range(N)]))
#       * (np.prod([1 - q[i]*x[i] for i in T])))
# m.options.SOLVER = 1
# m.solve()
# print(x)
