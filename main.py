from scipy.optimize import linprog

# Define the data matrix (replace with your actual data)
data = [
    [4, 5, 100, 150, 200],
    [3, 6, 120, 80, 150],
    [5, 3, 80, 100, 180]
]

# Define the constraints
machine1_capacity = [10, 8]  # Machine 1 capacity for Periods 1 and 2
machine2_capacity = [12, 9]  # Machine 2 capacity for Periods 1 and 2

workforce_requirements = [
    [2, 3],  # Workforce requirements for Product 1, Periods 1 and 2
    [1, 2],  # Workforce requirements for Product 2, Periods 1 and 2
    [3, 2]   # Workforce requirements for Product 3, Periods 1 and 2
]

max_workforce = [10, 12]  # Maximum available workforce for Periods 1 and 2

storage_requirements = [50, 30, 40]  # Storage requirements for Products 1, 2, and 3
max_storage_capacity = 100  # Maximum storage capacity

# Extracting necessary data for optimization
num_products = len(data)
num_periods = len(data[0]) - 3  # Accounting for time periods, demand, and profit columns

# Define the objective function coefficients
obj_coeffs = -1 * data[-1][3:]  # Using negative profit values to maximize profit

# Define the inequality constraints
ineq_constraints = []

# Machine capacity constraints
for period in range(num_periods):
    ineq_constraints.append([0] * (period * num_products) +
                            [data[i][period] for i in range(num_products)] +
                            [0] * (num_products * (num_periods - period - 1)) +
                            [0, 0])
    ineq_constraints.append([0] * (num_products * num_periods) +
                            [0, 0] +
                            [-machine1_capacity[period], 0])
    ineq_constraints.append([0] * (num_products * num_periods) +
                            [0, 0] +
                            [0, -machine2_capacity[period]])

# Workforce availability constraints
for period in range(num_periods):
    ineq_constraints.append([0] * (period * num_products) +
                            [workforce_requirements[i][period] for i in range(num_products)] +
                            [0] * (num_products * (num_periods - period - 1)) +
                            [0, 0])
    ineq_constraints.append([0] * (num_products * num_periods) +
                            [0, 0] +
                            [-max_workforce[period], 0])

# Storage constraints
for i in range(num_products):
    ineq_constraints.append([0] * (i * num_periods) +
                            [0] * num_periods +
                            [0, storage_requirements[i]])
ineq_constraints.append([0] * (num_products * num_periods) +
                        [0, -max_storage_capacity])

# Define the inequality constraint bounds (RHS values of the constraints)
ineq_bounds = [0] * (len(ineq_constraints) // 2) + [-bound for bound in ineq_constraints[len(ineq_constraints) // 2:]]
    
# Define the equality constraints (demand constraints)
eq_constraints = [[data[i][j] for j in range(num_periods)] + [0, 0] for i in range(num_products)]
    
# Define the equality constraint bounds (demand values)
eq_bounds = [data[i][-2] for i in range(num_products)]

# Define the bounds for the decision variables (production quantities)
bounds = [(0, None) for _ in range(num_products * num_periods)]

# Perform linear programming optimization
result = linprog(c=obj_coeffs,
                 A_ub=ineq_constraints,
                 b_ub=ineq_bounds,
                 A_eq=eq_constraints,
                 b_eq=eq_bounds,
                 bounds=bounds,
                 method='highs')

# Print the results
print("Optimal Production Plan:")
for i in range(num_products):
    for j in range(num_periods):
        print(f"Product {i+1} - Period {j+1}: {result.x[i*num_periods + j]} units")
    print()

print(f"Total Profit: ${-result.fun}")
