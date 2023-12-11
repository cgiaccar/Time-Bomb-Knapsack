"""
GEKKO solver for 01-TimeBomb-Knapsack problems.
Contains the solve_with_gekko function called in the main.

"""

import numpy as np
from gekko import GEKKO


def solve_with_gekko(w, p, c, q):

    n = len(w)  # number of items
    pi = [1-i for i in q]  # probability of NOT exploding
    T = [i for i in range(len(pi)) if pi[i] < 1]  # set of time-bomb items

    m = GEKKO(remote=False)  # create GEKKO model

    # variables
    x = [m.Var(lb=0, ub=1, integer=True) for j in range(n)]

    # constraint
    m.Equations([sum(w[j]*x[j] for j in range(n)) <= c])

    # objective function
    m.Maximize(sum(p[i]*x[i] for i in range(n)) *
               np.prod([1-(q[j]*x[j]) for j in T]))

    m.solve(disp=False)

    # unpack solution for readability before returning
    return ([item for items in x for item in items], -m.options.OBJFCNVAL, m.options.SOLVETIME)


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
    filenames = glob.glob("Data/generated-instances/*.txt")

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

    # Exception: @error: Max Equation Length
    # test_file = "Data/generated-instances/type3-500-0-0.5-9.txt"

    # sol is foud to be 0 (???)
    test_file = "Data/generated-instances/type3-100-0-0.5-9.txt"

    # print(f"{test_file = }")
    # print(f"n = {ns[test_file]}")
    # print(f"capacity = {capacities[test_file]}")
    # print(dataframes[test_file].head(3))  # first three rows

    w = dataframes[test_file]['weight'].tolist()
    p = dataframes[test_file]['profit'].tolist()
    q = dataframes[test_file]['probability'].tolist()
    c = int(capacities[test_file])

    par_x, par_obj, par_time = solve_with_gekko(w, p, c, q)
    print(
        f"\GEKKO solution:\nx = {par_x} \nobj = {par_obj} \ntime = {par_time:0.6f}")
