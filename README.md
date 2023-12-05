# Time-Bomb-Knapsack
Project for the Mathematical Optimization class on the paper "[Exact algorithms for the 0–1 Time-Bomb Knapsack Problem](https://www.sciencedirect.com/science/article/pii/S0305054822001253)" 

## Code Organization
- **Time-Bomb-Knapsack/**

    - **Data/**

        - **generated-instances/** (problems from the paper)

        - **data.py** (code to load the data)

    - **Subset_enumeration_alg.py** (working implementation of the first algorithm of the paper)

    - **Parallel_subset_enum_alg.py** (parallelization of the first algorithm of the paper)

    - **gekko_solver.py** (working problem formalization in GEKKO)

    - **gurobi_solver_01_KP.py** (01-Knapsack implementation in Gurobi, used in the enumeration algorithms)

    - **main.py** (runs all solvers and algorithms on some small problems to test the results)

    - **Discarded code/** (stuff I started implementing that is not useful anymore; contains non-working formalizations of the problem in Gurobi and SciPy, everything regarding the Branch&Bound algorithm of the paper and a try at the DP approach)

    - **README.md**