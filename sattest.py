from numpy import var
from z3 import *

list = [0,1,2,3]
for i in range(len(list)-1,-1,-1):
    for j in range(len(list)-1,i-1,-1):
        print(i,j)