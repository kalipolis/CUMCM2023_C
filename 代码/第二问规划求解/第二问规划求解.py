from scipy.optimize import minimize
import pandas as pd

def optimize(b, k, loss, discount, cost, X_low, Y_low, Y_high):
    # 目标函数
    def objective_function(variables):
        X, Y = variables
        Z = -(b-k*Y)*(1-loss)*Y - (b-k*Y)*loss*discount*Y + X*cost
        return Z

    # 约束条件
    constraints = (
        {'type': 'ineq', 'fun': lambda variables: variables[0] - X_low},  # X>=X_low
        {'type': 'ineq', 'fun': lambda variables: variables[1] - Y_low},  # Y>=Y_low
        {'type': 'ineq', 'fun': lambda variables: -variables[1] + Y_high},  # Y<=Y_high
        {'type': 'ineq', 'fun': lambda variables: variables[0] - (b-k*variables[1])}  # b-k*Y<=X
    )

    # 初始猜测
    initial_guess = [10, (Y_low+Y_high)/2]

    # 求解
    solution = minimize(objective_function, initial_guess, constraints=constraints)

    # 输出结果
    print(f"The optimal value of X is: {solution.x[0]}")
    print(f"The optimal value of Y is: {solution.x[1]}")

# 使用不同参数运行优化
print('-'*40)


# 读取Excel文件
df = pd.read_excel('最优化系数表.xlsx', sheet_name='食用菌')

# 遍历每一行
for index, row in df.iterrows():
    b = row['b']
    k = row['k']
    loss = row['loss']
    discount = row['discount']
    cost = row['cost']
    X_low = row['X_low']
    Y_low = row['Y_low']
    Y_high = row['Y_high']

    # 调用优化函数
    optimize(b, k, loss, discount, cost, X_low, Y_low, Y_high)
    print('-' * 40)