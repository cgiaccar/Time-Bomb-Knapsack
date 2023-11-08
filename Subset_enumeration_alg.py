#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:19:53 2023

Implementation of the first algorithm from the paper:
    Subset Enumeration
For each subset of time-bomb items S ⊆ T, such that ∑j∈S of w_j ≤ c,
consider the solution obtained by (i) forcing in the solution all items in the
current set S; (ii) forbidding all remaining time-bomb items (i.e., those in
set T⧵S); and (iii) completing the solution using some deterministic items.
In particular, in the last step, we solve a deterministic 01-KP instance
defined by the deterministic items and a capacity equal to c − ∑j∈S of w_j.
Then, an optimal solution for the 01-TB-KP is obtained taking the best among
all these solutions.

!!!! No errors, but it's not working, the result is wrong !!!!

@author: Camilla
"""

import math

# this import doesn't work; la funzione è stata copia-incollata qui
# import gurobi_solver_01-KP
import gurobipy as gb

from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


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
    return knapsack_model.objVal


def TBE_num(n, w, p, pi, c):
    T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items (?)
    T_prime = [pi.index(j) for j in pi if j >= 1]   # deterministic items
    z_opt = 0
    w_det = [w[i] for i in T_prime]  # weight of deterministic items
    p_det = [p[i] for i in T_prime]  # profit of deterministic items

    for S in powerset(T):  # Enumerate all time-bomb item subsets
        if sum(w[j] for j in S) <= c:  # Discard trivial cases
            d = solve_deterministic_01KP(w_det, p_det, c-sum(w[j] for j in S))
            z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

            if z > z_opt:
                z_opt = z  # Update the best solution value

    return z_opt


w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
# q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
q = [0, 0, 0, 0, 0, 0, 0, 0]  # all zeros --> standard knapsack
pi = [1-i for i in q]  # probability of NOT exploding
c = 15  # capacity
n = len(w)  # number of items

T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items

print(TBE_num(n, w, p, pi, c))
