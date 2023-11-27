"""
Gurobi solver for 01-Knapsack problems.
Contains the solve_deterministic_01KP function (used by the exact algorithms) and some examples to test it.

"""

import gurobipy as gb


def solve_deterministic_01KP(w, p, c):

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
    return (knapsack_model.x, knapsack_model.objVal)


# FOR TESTING

# simple example
# w = [8, 5, 10]  # weight
# p = [4, 2, 5]  # profit
# c = 15

# another example
w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]  # weight
p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]  # profit
c = 77

# used example
# w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
# p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
# c = 15  # capacity

print(solve_deterministic_01KP(w, p, c))
