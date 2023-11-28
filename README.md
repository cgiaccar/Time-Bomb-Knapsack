# Time-Bomb-Knapsack
Project for the Mathematical Optimization class on the paper "[Exact algorithms for the 0–1 Time-Bomb Knapsack Problem](https://www.sciencedirect.com/science/article/pii/S0305054822001253)" 

## Code Organization
- **Time-Bomb-Knapsack/**

    - **Data/**

        - **generated-instances/** (problems from the paper)

        - **data.py** (code to load the data)

    - **Dynamic_programming_alg.py** (first try at the DP approach of the paper)  

    - **Subset_enumeration_alg.py** (working implementation of the first algorithm of the paper)

    - **gekko_solver.py** (working problem formalization in GEKKO)

    - **gurobi_solver_01_KP.py** (01-Knapsack implementation in Gurobi, used in Subset_enumeration_alg)

    - **main.py** (runs SubsetEnum, gekko and gurobi on some small problems to test the results)

    - **Discarded code/** (stuff I started implementing that is not useful anymore; contains try_with_scipy.py, a non-working formalization of the problem in Gurobi and everything regarding the Branch&Bound algorithm of the paper)

    - **README.md**