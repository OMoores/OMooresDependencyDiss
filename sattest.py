from numpy import var
from z3 import *
solver = Solver()

arr = [1,2,3]
T = Int('f{x}')

z3_array = Array('z3_array', IntSort(), IntSort())
for i, value in enumerate(arr):
    z3_array = Store(z3_array, i, value)

solver.add(Select(z3_array, T) == 2)


print(solver.check())
model = solver.model()
for item in model.decls():
    print(model[item])