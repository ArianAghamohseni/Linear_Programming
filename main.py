from scipy.optimize import linprog
import numpy as np


# Constants


profits = [1500, 2200, 1200, 3400, 2500, 1100]  # Profit for each product in each period
storage_expenses = [-14, -21, -20, -22, -19, -31]  # Storage expense for each product in each period
storage_capacities = [230, 550, 370, 540, 700, 600]  # Storage capacity for each product in each period

time_consumption_by_machine = [7, 11, 10, 12, 8, 8]  # Time consumed by each product on each machine
max_times_for_machines = [11000, 22000, 20000, 19000]  # Maximum available time for each machine in each period

workers_per_product = [20, 15, 18, 22, 21, 18]  # Workforce requirements for producing each product in each period
max_workers = [65000, 55000]  # Maximum available workforce in each period

demands = [120, 142, 160, 200, 123, 210]  # Demand forecast for each product in each period


def solve(
    profits=profits,
    storage_expenses=storage_expenses,
    storage_capacities=storage_capacities,
    time_consumption_by_machine=time_consumption_by_machine,
    max_times_for_machines=max_times_for_machines,
    workers_per_product=workers_per_product,
    max_workers=max_workers,
    demands=demands
):

    b_ub = []
    A_ub = []
    A_eq = []
    b_eq = []

    # Objective Function

    c = [*profits[:3]*2, *profits[3:]*2, *storage_expenses]
    c = list(map(lambda x:x*(-1), c))


    # Constraints

    # Max Time Each Machine
    A_ub.append([0]*0 + time_consumption_by_machine[:3] + [0]*15)
    A_ub.append([0]*3 + time_consumption_by_machine[3:] + [0]*12)
    A_ub.append([0]*6 + time_consumption_by_machine[:3] + [0]*9)
    A_ub.append([0]*9 + time_consumption_by_machine[3:] + [0]*6)


    b_ub += max_times_for_machines

    # Maxi Workeforce Each Period
    A_ub.append([0]*0 + workers_per_product[:3]*2 + [0]*12)
    A_ub.append([0]*6 + workers_per_product[3:]*2 + [0]*6)


    b_ub += max_workers

    # Demand would Be Satisfied

    A_eq.append([1,0,0,1,0,0] + [0]*6 + [-1,0,0,0,0,0])
    A_eq.append([0,1,0,0,1,0] + [0]*6 + [0,-1,0,0,0,0])
    A_eq.append([0,0,1,0,0,1] + [0]*6 + [0,0,-1,0,0,0])
    A_eq.append([0]*6 + [1,0,0,1,0,0] + [1,0,0,-1,0,0])
    A_eq.append([0]*6 + [0,1,0,0,1,0] + [0,1,0,0,-1,0])
    A_eq.append([0]*6 + [0,0,1,0,0,1] + [0,0,1,0,0,-1])

    b_eq += demands

    # 4. Bounds

    bounds = (
        (0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
        (0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
        (0,storage_capacities[0]),
        (0,storage_capacities[1]),
        (0,storage_capacities[2]),
        (0,storage_capacities[3]),
        (0,storage_capacities[4]),
        (0,storage_capacities[5])
        )


    # Solve

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, integrality=[1]*18, method="highs")

    # Optimal solution
    optimal_solution = result.x


    try:
        print("Max Profit:", -result.fun)

        optimal_solution = list(map(round, optimal_solution))
        optimal_solution = np.array(optimal_solution).reshape(3, 2, 3)

        for period in range(0, 2):
            print(f'Period {period+1}:')

            # Print storage information
            print('  Storage:', end='')
            for i in range(len(optimal_solution[-1][0-period])):
                print(f" Product {i+1}: {optimal_solution[-1][0-period][i]}", end='\t')
            print()

            # Print product and machine allocation information
            for machine in range(0, 2):
                for product in range(0, 3):
                    print(f"  Product {product+1} with Machine {machine+1}: {optimal_solution[period][machine][product]}")

            print()

    except:
        print("The Problem cannot be solved!")

    finally:
        print("Done\n")



# Full Explanation in wiki


# First Condition

M = 10**5
solve(storage_expenses=[-10,-20,-30,-M,-M,-M])


# Seconde Condition

solve()



# Sensitivity Analysis on Worker Constraints

max_worker_in_each_period = [40000, 350]
solve(max_workers=max_worker_in_each_period)

max_worker_in_each_period = [40000, 0]
solve(max_workers=max_worker_in_each_period)

max_worker_in_each_period = [4000, 35000]
solve(max_workers=max_worker_in_each_period)


# Sensitivity Analysis on Machine Constraints


max_time_for_each_machine_in_each_period = [100000, 20000, 20000, 10000]
solve(max_times_for_machines=max_time_for_each_machine_in_each_period)

max_time_for_each_machine_in_each_period = [10000, 20000, 20000, 10000]
solve(max_times_for_machines=max_time_for_each_machine_in_each_period)

max_time_for_each_machine_in_each_period = [1000, 3000, 20000, 10000]
solve(max_times_for_machines=max_time_for_each_machine_in_each_period)

max_time_for_each_machine_in_each_period = [1000, 2000, 20000, 10000]
solve(max_times_for_machines=max_time_for_each_machine_in_each_period)

max_time_for_each_machine_in_each_period = [10000, 2000, 200, 100]
solve(max_times_for_machines=max_time_for_each_machine_in_each_period)
