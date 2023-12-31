"""
Gurobi solver for 01-Knapsack problems.
Contains the solve_deterministic_01KP function used by the exact algorithms.

"""

import gurobipy as gb


def solve_deterministic_01KP(w, p, c):
    # set environment to avoid printing license
    with gb.Env(empty=True) as env:
        env.setParam('OutputFlag', 0)
        env.start()

        n = len(w)  # number of items

        # optimization model
        knapsack_model = gb.Model(env=env)

        # add decision variables
        x = knapsack_model.addVars(n, vtype=gb.GRB.BINARY, name="x")

        # add the constraints
        knapsack_model.addConstr(sum(w[j]*x[j] for j in range(n)) <= c)

        # objective function
        obj_fn = sum(p[j]*x[j] for j in range(n))
        knapsack_model.setObjective(obj_fn, gb.GRB.MAXIMIZE)

        # solve the model and output the solution
        knapsack_model.optimize()
        return (knapsack_model.x, knapsack_model.objVal, knapsack_model.Runtime)
