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

gekko_sol = solve_with_gekko(w, p, c, q)
enum_sol = TBEnum(w, p, c, q)
gurobi_sol = solve_deterministic_01KP(w, p, c)

print("Using \"another example\"")
print("\nGEKKO solution:\nx = %s \nobj = %s \ntime = %s" %
      (gekko_sol[0], gekko_sol[1], gekko_sol[2]))
print("\nSubset Enumeration algorithm solution:\nx = %s \nobj = %s \ntime = %s" %
      (enum_sol[0], enum_sol[1], enum_sol[2]))
print("\nSimple Gurobi solution:\nx = %s \nobj = %s \ntime = %s" %
      (gurobi_sol[0], gurobi_sol[1], gurobi_sol[2]))
