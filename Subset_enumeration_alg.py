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
    return (knapsack_model.x, knapsack_model.objVal)


def TBE_num(n, w, p, pi, c):
    T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items
    T_prime = [i for i in range(len(pi)) if pi[i] >= 1]  # deterministic items
    z_opt = 0
    x_opt = []
    w_det = [w[i] for i in T_prime]  # weight of deterministic items
    p_det = [p[i] for i in T_prime]  # profit of deterministic items

    for S in powerset(T):  # Enumerate all time-bomb item subsets
        if sum(w[j] for j in S) <= c:  # Discard trivial cases
            (x, d) = solve_deterministic_01KP(
                w_det, p_det, c-sum(w[j] for j in S))
            z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

            if z > z_opt:
                z_opt = z  # Update the best solution value
                x_opt = [S]
                x_opt.append(x)

    return (x_opt, z_opt)


# simple example
# w = [8, 5, 10]  # weight
# p = [4, 2, 5]  # profit
# q = [0.1, 0.9, 0]  # probability of exploding
# q = [0, 0, 0]  # all zeros --> standard knapsack
# c = 15

# another example
w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]  # weight
p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]  # profit
q = [0.5, 0, 0.9, 0, 0.2, 0.6, 0.4, 0.3, 0, 1]  # probability of exploding
# q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # all zeros --> standard knapsack
c = 77

# used example
# w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
# p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
# q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
# q = [0, 0, 0, 0, 0, 0, 0, 0]  # all zeros --> standard knapsack
# c = 15  # capacity

pi = [1-i for i in q]  # probability of NOT exploding
n = len(w)  # number of items
T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items

print(TBE_num(n, w, p, pi, c))
