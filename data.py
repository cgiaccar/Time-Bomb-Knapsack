#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 19:25:36 2023

Code to load all the files into dataframes
This will create three dictionaries with the name of the file as key and value:
    its n in ns,
    its capacity in capacities
    and its corresponding dataframe in dataframes.

@author: Camilla
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
filenames = glob.glob("generated-instances/*.txt")

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
test_file = "generated-instances/type3-5000-0-0.5-9.txt"
print(f"{test_file = }")
print(f"n = {ns[test_file]}")
print(f"capacity = {capacities[test_file]}")
print(dataframes[test_file].head(3))  # first three rows
