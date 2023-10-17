#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 19:16:22 2023

Exception: @error: Inequality Definition
 invalid inequalities: z > x < y
 maximize((((((((((0+((10)*(int_v1)))+((5)*(int_v2)))+((18)*(int_v3)))+((12)*(in
 t_v4)))+((15)*(int_v5)))+((1)*(int_v6)))+((2)*(int_v7)))+((8)*(int_v8))))*(<gen
 eratorobject<genexpr>at0x7f806d1c8ac0>))
 STOPPING . . .

@author: Camilla
"""
import numpy as np
from gekko import GEKKO

w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
pi = [1-i for i in q]  # probability of NOT exploding
c = 15  # capacity
n = len(w)  # number of items

T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items
print(T)
print(len(T))


m = GEKKO(remote=False)  # create GEKKO model

x = [m.Var(lb=0, ub=1, integer=True) for j in range(n)]
alpha = [m.Var(lb=0, ub=1) for j in range(len(T))]
m.Equations([sum(w[j]*x[j] for j in range(n)) <= c])
m.Equations([alpha[j] == 1-q[j]*x[j] for j in range(len(T))])
m.Maximize(sum(p[j]*x[j] for j in range(n))
           * (np.prod(alpha[j] for j in range(len(T)))))

m.solve(disp=True)
print(x)  # print solution


###################### SIMPLE FOUND ONLINE ##########################

# from gekko import GEKKO
# m = GEKKO(remote=False)  # create GEKKO model
# x = m.Var()            # define new variable, default=0
# y = m.Var()            # define new variable, default=0
# m.Equations([3*x+2*y == 1, x+2*y == 0])  # equations
# m.solve(disp=False)    # solve
# print(x.value, y.value)  # print solution

######################################################################


###################### TUTOR WITH PAPER ##########################

# import random
# import numpy as np
# from gekko import GEKKO
# np.random.seed(0)
# random.seed(0)

# N = 10
# frac = 2
# T = np.random.choice(range(N), N//frac)

# print(T)

# q = np.random.uniform(0, 0.99999, size=N)  # il prof aveva scritto size=len(T)
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

##################################################################


###################### TUTOR FOUND ONLINE ##########################

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

#######################################################################
