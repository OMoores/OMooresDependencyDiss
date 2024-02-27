from numpy import var
from z3 import *
# Create a solver
solver = Solver()
int_values = [1,2,3]
# Example lists (replace these with your actual data)
symbolic_indices = Array('symbolic_indices',IntSort(), IntSort())
for i in range(len(int_values)):
    symbolic_indices = Store(symbolic_indices,i,int_values[i])

z = Int('number')
solver.add(z >= 0)
solver.add(z < len(int_values))


solver.add(Select(symbolic_indices, z) == 2)

print(solver.check())