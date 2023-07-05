#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:13:20 2023

Implementation of the second algorithm from the paper:
    Branch & Bound

@author: Camilla
"""

import math
import gurobipy as gb


# select the unfixed time-bomb item, say chosen_j , with the largest p_j∕w_j
# ratio and which fits in the residual capacity
def choose_TB_item(items, w, p, c):
    max_ratio = 0
    current_ratio = 0
    chosen_j = 0
    for j in items:
        if w[j] < c:
            current_ratio = p[j]/w[j]
            if max_ratio < current_ratio:
                max_ratio = current_ratio
                chosen_j = j
    return chosen_j


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


def compute_lower_bound(item_set, capacity):
    return None


def compute_upper_bound(item_set, capacity):
    return None


def Explore_Node(T_prime, p, pi, n, c, w, T, S, S_neg, z_opt):
    item_set = [j for j in range(1, n+1) if j not in S+S_neg]
    knapsack_capacity = c - sum(w[j] for j in S)
    z_low = compute_lower_bound(item_set, knapsack_capacity)
    z_upp = compute_upper_bound(item_set, knapsack_capacity)

    if z_low > z_opt:
        z_opt = z_low

    if z_upp <= z_opt:
        return None  # prune, so quit this procedure for the current node

    if not [i for i in T if i not in S+S_neg]:  # empty lists are always false
        w_det = [w[i] for i in T_prime]  # weight of deterministic items
        p_det = [p[i] for i in T_prime]  # profit of deterministic items
        d = solve_deterministic_01KP(w_det, p_det, c-sum(w[j] for j in S))
        z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

        if z > z_opt:
            z_opt = z
    else:
        # 'items' is the unfixed time-bomb items to chose from
        items = [j for j in T if j not in S+S_neg]
        chosen_j = choose_TB_item(items, w, p, c-sum(w[j] for j in S))
        Explore_Node(T_prime, p, pi, n, c, w, T,
                     S.append(chosen_j), S_neg, z_opt)
        Explore_Node(T_prime, p, pi, n, c, w, T, S,
                     S_neg.append(chosen_j), z_opt)

    return None


def TB_Branch_Bound(n, w, p, pi, c):
    T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items (?)
    T_prime = [pi.index(j) for j in pi if j >= 1]   # deterministic items
    S = 0
    S_neg = 0
    z_opt = 0

    Explore_Node(T_prime, p, pi, n, c, w, T, S, S_neg, z_opt)
    return z_opt
