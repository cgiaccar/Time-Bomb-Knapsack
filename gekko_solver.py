import numpy as np
from gekko import GEKKO

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


m = GEKKO(remote=False)  # create GEKKO model

# variables
x = [m.Var(lb=0, ub=1, integer=True) for j in range(n)]

# constraint
m.Equations([sum(w[j]*x[j] for j in range(n)) <= c])

# objective function
m.Maximize(sum(p[i]*x[i] for i in range(n)) *
           np.prod([1-(q[j]*x[j]) for j in T]))

m.solve(disp=True)
print(x)  # print solution
