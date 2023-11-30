"""
This files contains some tests for the solvers in the form of different problems.

"""

from gekko_solver import solve_with_gekko
from Subset_enumeration_alg import TBEnum
from gurobi_solver_01_KP import solve_deterministic_01KP

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

gekko_x, gekko_obj, gekko_time = solve_with_gekko(w, p, c, q)
enum_x, enum_obj, enum_time = TBEnum(w, p, c, q)
gurobi_x, gurobi_obj, gurobi_time = solve_deterministic_01KP(w, p, c)

print("Using \"another example\"")
print(
    f"\nGEKKO solution:\nx = {gekko_x} \nobj = {gekko_obj} \ntime = {gekko_time:0.6f}")
print(
    f"\nSubset Enumeration algorithm solution:\nx = {enum_x} \nobj = {enum_obj} \ntime = {enum_time:0.6f}")
print(
    f"\nSimple Gurobi solution:\nx = {gurobi_x} \nobj = {gurobi_obj} \ntime = {gurobi_time:0.6f}")
