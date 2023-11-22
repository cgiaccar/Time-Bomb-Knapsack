w = [4, 2, 5, 4, 5, 1, 3, 5]  # weight
p = [10, 5, 18, 12, 15, 1, 2, 8]  # profit
q = [0, 0, 0.2, 0.5, 0.8, 0.1, 0, 0.7]  # probability of exploding
# q = [0, 0, 0, 0, 0, 0, 0, 0]  # all zeros --> standard knapsack
pi = [1-i for i in q]  # probability of NOT exploding
c = 15  # capacity
n = len(w)  # number of items

T = [pi.index(j) for j in pi if j < 1]  # set of time-bomb items
T_prime = [pi.index(j) for j in pi if j >= 1]   # deterministic items

T_convenienza = range(1, len(T)+1)

w_exploding = [w[i] for i in T]
p_exploding = [p[i] for i in T]
w_det = [w[i] for i in T_prime]
p_det = [p[i] for i in T_prime]
# U = solve_deterministic_01KP(w, p, c)

d = 0
v = 0
v_calcolato = solve_deterministic_01KP(w_exploding, p_exploding, d)
x = solve_deterministic_01KP(w_exploding, p_exploding, d).x  # TODO
x_ones = [i for i in range(len(x)) if x[i] == 1]

pi_trattino = max(pi[i] for i in x_ones)

v_calcolato >= v


def find_pi(d, v, j):
    if (v == 0 & j == 0):
        return 1
    elif (v >= 1 & j == 0):
        return 0
    else:
        return max(find_pi(d, v, j-1), find_pi(max(d-w[j], 0), max(v-p[j], 0), j-1)*pi[j])


def first_alg(w_exploding, p_exploding, d, v):
    pi_trattino = 0
    sol = solve_deterministic_01KP(w_exploding, p_exploding, d)
    if (sol != False & sol.v >= v):
        x = sol.x
        x_ones = [i for i in range(len(x)) if x[i] == 1]
        pi_trattino = find_pi(d, v, j)
        # pi_trattino = max(pi[i] for i in x_ones) ??????
    return pi_trattino


def second_alg(w_det, p_det, cap):
    return solve_deterministic_01KP(w_det, p_det, cap)  # z(c-d)


def DP_alg():
    U = solve_deterministic_01KP(w_exploding, pi_exploding, c)  # upper buond
    result = 0
    for d in range(c):
        for v in range(U):
            z = second_alg(c-d)
            pi = find_pi(d, v, t)
            result = max(result, (v+z)*pi)
    return result
