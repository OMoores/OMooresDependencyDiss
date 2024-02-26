from numpy import var
from z3 import *
solver = Solver()

def distinct(list):
    if len(set(list)) == len(list):
        return True
    return False

list = [1,2,3,4]

variables = [Int(f'x{i}') for i in range(len(list))]

for i in range(len(variables)):
    solver.add(Or([variables[i] == list[j] for j in range(len(variables))]))

for i in range(len(variables)-1):
    solver.add(variables[i] > variables[i+1])

solver.check()
m=solver.model()

print([m.evaluate(num).as_long() for num in variables])
