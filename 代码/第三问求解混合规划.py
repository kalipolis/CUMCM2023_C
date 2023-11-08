from pyomo.environ import *

# 假设你的销量和成本是如下列表
loss = [9.43, 9.43, 9.43, 0.45, 5.7, 13.62, 9.26, 9.43, 9.43, 6.07, 2.48, 0.2, 18.52, 0, 9.43, 9.43, 10.18, 15.68, 5.54, 7.61, 10.33, 10.8, 8.42, 6.9, 24.05, 14.43, 9.43, 29.25, 5.01, 9.43, 9.43, 9.43, 9.61, 15.25, 13.7, 0.84, 6.71, 9.43, 18.51, 26.16, 9.43, 12.81, 16.63, 6.57, 9.43, 9.43, 12.69, 9.43, 9.43]
discount = [
    0.65, 0.9, 0.65, 0.25, 0.9, 0.65, 0.7, 0.9, 0.9, 1,
    0.65, 0.25, 0.65, 0.25, 0.65, 0.9, 0.9, 0.65, 0.75, 0.65,
    0.65, 0.25, 0.65, 1, 0.75, 0.65, 0.7, 0.75, 1, 0.25,
    0.9, 0.9, 0.75, 0.65, 0.65, 0.25, 1, 0.9, 0.65, 0.65,
    0.75, 0.65, 0.75, 0.25, 0.25, 0.65, 0.75, 0.9, 1
]
costs = [3.312929, 2.1480732, 2.7906902, 1.529059, 3.643471, 2.1485615, 7.509555, 2.0952864, 4.1853228, 3.5173018, 4.350702, 3.4483738, 2.2697756, 2.1510348, 3.9503517, 2.278803, 8.915366, 2.5471723, 10.159343, 3.0883691, 2.7038798, 14.621622, 2.6660647, 6.967654, 18.26312, 4.171282, 8.33144, 11.63622, 4.062099, 2.799846, 3.3154902, 12.528717, 9.257743, 5.49638, 4.608606, 3.2926397, 3.3574264, 12.254727, 9.377361, 9.229966, 13.079778, 2.8454483, 5.6507764, 3.2716556, 1.4350971, 1.8988357, 13.232207, 2.4916992, 4.529908]
b = [253.26, 99.91381329, 253.26, 114.208, 106.217, 208.2352953, 108.0085258, 94.55101947, 104.9468922, 30.149, 218.909282, 114.208, 203.4539719, 110.3860095, 253.26, 91.77312022, 88.13566734, 182.5684573, 114.2247663, 215.1357071, 208.6576165, 149.7613804, 211.3529213, 33.44705117, 77.79054151, 168.3037318, 63.621, 56.56402989, 29.00174565, 103.0453738, 97.90771035, 99.55691831, 67.52447217, 206.492586, 196.7594758, 108.3557882, 27.66291403, 96.54315535, 191.4273616, 226.3282624, 64.56349557, 202.4038979, 66.93711879, 82.55280318, 107.0579974, 250.9536667, 69.47588225, 98.41338121, 30.149]
k = [-12.542, -0.785145254, -12.542, -5.14, -2.523, -9.798806107, 1.234899831, -1.85353454, -1.919284672, -0.999, -11.66341446, -5.14, -9.573191636, -4.803437508, -12.542, -1.437039677, -0.487353742, -6.866286949, -1.344851036, -10.16333416, -9.278707543, -5.779804623, -9.875691377, -0.72623816, -3.225574227, -5.526521269, -2.664, -2.295836371, -0.646402124, -4.08695077, -1.996443187, -2.245301009, -3.178902375, -6.522332136, -8.93198424, -4.72634013, -0.837037267, -2.164214731, -7.895684758, -10.89960348, -2.892283772, -8.35407298, -3.134538433, -2.364805547, -4.733331191, -12.41950807, -3.29369461, -2.172442172, -0.999]
hcl = [6, 26]
hyl = [0, 2, 5, 10, 12, 14, 17, 19, 20, 22, 25, 33, 34, 38, 39, 41, 45]
ljl = [1, 4, 7, 8, 15, 16, 30, 31, 37, 47]
ql = [1, 4, 7, 8, 15, 16, 30, 31, 37, 47]
syj = [3, 11, 13, 21, 29, 35, 43, 44]
ssgjl = [18, 24, 27, 32, 40, 42, 46]


model = ConcreteModel()

model.q = Var(range(49), domain=Binary, initialize=0)
model.prices = Var(range(49), domain=NonNegativeReals, bounds=(2, 25), initialize=10)
model.inventories = Var(range(49), domain=NonNegativeReals, bounds=(2.5, 50), initialize=2.5)

#考虑损耗率的目标函数
model.obj = Objective(
    expr=sum(model.q[i] * (b[i] + k[i] * model.prices[i]) * model.prices[i] * (1 - 0.01 * loss[i]) + model.q[i] * (b[i] - k[i] * model.prices[i]) * model.prices[i] * 0.01 * loss[i] * discount[i] - model.q[i] * costs[i] * model.inventories[i] for i in range(49)),
    sense=maximize)

# 不考虑损耗率的目标函数
# model.obj = Objective(
#     expr=sum(model.q[i] * (b[i] + k[i] * model.prices[i]) * model.prices[i] - model.q[i] * costs[i] * model.inventories[i] for i in range(49)),
#     sense=maximize)

# Constraints
model.constraint1 = Constraint(expr=sum(model.q[i] for i in range(49)) >= 27)
model.constraint2 = Constraint(expr=sum(model.q[i] for i in range(49)) <= 33)

# 销售量 <= 进货量
model.constraint3 = ConstraintList()
for i in range(49):
    model.constraint3.add((b[i] - k[i] * model.prices[i]) <= model.inventories[i])

# # 各品类销量不小于某值
model.constraint4 = Constraint(expr=sum(mventories[i] for i in ssgjl) >= 10.384)

# # 各品类进货量不小于某值
model.constraint4 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in hcl) >= 8.083)
model.constraint5 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in hyl) >= 80.524)
model.constraint6 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in ljl) >= 67.12)
model.constraint7 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in ql) >= 8.415)
model.constraint8 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in syj) >= 35.271)
model.constraint9 = Constraint(expr=sum(model.q[i] * model.inventories[i] for i in syj) >= 10.384)
SolverFactory('bonmin').solve(model)

# Print the results
for i in range(49):
    print(f'Product {i+1}: q = {model.q[i].value}, price = {model.prices[i].value}, inventory = {(b[i] + k[i] * model.inventories[i].value)}')

