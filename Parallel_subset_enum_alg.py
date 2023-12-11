"""
First algorithm implementation from the paper:
    Subset enumeration algorithm to solve 01-TimeBomb-Knapsack problems.
Contains some utilities and the TBEnum function described in the paper.

Parallelized version. Can be called by the main or run as is.

"""

import math
from itertools import chain, combinations
from time import perf_counter
import multiprocessing as mp
from gurobi_solver_01_KP import solve_deterministic_01KP


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def update_x_opt(n, S, x, T_prime):
    x_opt = [0 for i in range(n)]
    for index in S:
        x_opt[index] = 1
    i = 0
    for index in T_prime:
        if x[i] == 1:
            x_opt[index] = 1
        i += 1
    return x_opt


def divide_in_chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]


def wrapper(tup):
    """Since pool.map needs a single argument, wrapper calls the function after unpacking the arguments"""
    return find_opt_in_chunk(*tup)


def find_opt_in_chunk(chunk, w, c, w_det, p_det, p, pi, z_opt, x_opt, n, T_prime):
    for S in chunk:  # Enumerate all time-bomb item subsets
        if sum(w[j] for j in S) <= c:  # Discard trivial cases
            (x, d, _) = solve_deterministic_01KP(
                w_det, p_det, c-sum(w[j] for j in S))
            z = (d + sum(p[j] for j in S)) * (math.prod(pi[j] for j in S))

            if z > z_opt:
                z_opt = z  # Update the best solution value
                x_opt = update_x_opt(n, S, x, T_prime)

    return x_opt, z_opt


def ParTBEnum(w, p, c, q):
    if __name__ == 'Parallel_subset_enum_alg' or __name__ == '__main__':
        start_time = perf_counter()

        n = len(w)  # number of items
        pi = [1-i for i in q]  # probability of NOT exploding
        T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items
        # deterministic items
        T_prime = [i for i in range(len(pi)) if pi[i] >= 1]

        z_opt = 0
        x_opt = [0 for i in range(n)]
        w_det = [w[i] for i in T_prime]  # weight of deterministic items
        p_det = [p[i] for i in T_prime]  # profit of deterministic items

        # divide powerset(T) in a number of chunks depending on cpus
        chunks = list(divide_in_chunks([*powerset(T)], mp.cpu_count()))

        # create a single object combining chunk and necessary parameters
        arguments = [(chunk, w, c, w_det, p_det, p, pi, z_opt,
                      x_opt, n, T_prime) for chunk in chunks]

        # create a process pool that uses all cpus
        with mp.Pool(mp.cpu_count()) as pool:

            # call the function for each item in parallel and take results
            x_results, z_results = zip(
                *pool.map(wrapper, arguments))

            z_opt = max(z_results)  # find max z
            opt_index = z_results.index(z_opt)  # get its index
            x_opt = x_results[opt_index]  # get corresponding solution

        end_time = perf_counter()
        return (x_opt, z_opt, end_time-start_time)


if __name__ == '__main__':

    # piece of code taken from the main

    # # another example
    # w = [23, 10, 15, 35, 20, 60, 52, 16, 17, 28]  # weight
    # p = [30, 5, 43, 17, 20, 100, 42, 24, 13, 300]  # profit
    # q = [0.5, 0, 0.9, 0, 0.2, 0.6, 0.4, 0.3, 0, 1]  # probability of exploding
    # # q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # all zeros --> standard knapsack
    # c = 77

    """
    Code to load all the files into dataframes
    This will create three dictionaries with the name of the file as key and value:
        its n in ns,
        its capacity in capacities
        and its corresponding dataframe in dataframes.

    """

    import glob
    import pandas as pd

    # Import as a df the first txt file
    # file = 'generated-instances/type1-100-0-0.1-1.txt'
    # cols = ['weight', 'profit', 'probability']
    # dataframe = pd.read_csv(file, sep=r"\s+", names=cols, skiprows=1,header=None)
    # header = pd.read_csv(file, nrows=0,  usecols=[0])
    # header = header.columns.values[0].split()
    # n = header[0]
    # capacity = header[1]
    # print(f"{n = }")
    # print(f"{capacity = }")
    # print(dataframe)

    # Now import everything

    # All files and directories ending with .txt and that don't begin with a dot:
    filenames = glob.glob("Data/generated-instances/type1-100-0-0.1-1.txt")

    # empty dictionaries to store n, capacity and dataframe from each file
    ns = dict()
    capacities = dict()
    dataframes = dict()
    cols = ['weight', 'profit', 'probability']

    # iterate to fill the dictionaries
    for file in filenames:
        dataframe = pd.read_csv(file, sep=r"\s+", names=cols,
                                skiprows=1, header=None)
        header = pd.read_csv(file, nrows=0,  usecols=[0])
        header = header.columns.values[0].split()
        ns[file] = header[0]
        capacities[file] = header[1]
        dataframes[file] = dataframe

    # test print to check if it worked
    test_file = "Data/generated-instances/type1-100-0-0.1-1.txt"
    # print(f"{test_file = }")
    # print(f"n = {ns[test_file]}")
    # print(f"capacity = {capacities[test_file]}")
    # print(dataframes[test_file].head(3))  # first three rows

    w = dataframes[test_file]['weight'].tolist()
    p = dataframes[test_file]['profit'].tolist()
    q = dataframes[test_file]['probability'].tolist()
    c = int(capacities[test_file])

    # [Done] exited with code=null in 43.44 seconds
    # w = w[:len(w)//2]
    # p = p[:len(p)//2]
    # q = q[:len(q)//2]

    # [Done] exited with code=null in 36.296 seconds
    # w = w[:len(w)//3]
    # p = p[:len(p)//3]
    # q = q[:len(q)//3]

    # Memoria computer esaurita ([Done] exited with code=null in 81.176 seconds)
    w = w[:len(w)//4]
    p = p[:len(p)//4]
    q = q[:len(q)//4]

    print(len(w))
    print(len(p))
    print(len(q))

    print(type(c))
    print(type(w[0]))

    par_x, par_obj, par_time = ParTBEnum(w, p, c, q)
    print(
        f"\nParallel Subset Enumeration algorithm solution:\nx = {par_x} \nobj = {par_obj} \ntime = {par_time:0.6f}")
