from src.Recommendations import *
import random

depWeb = [[3,2,3,3,3],[0,3,3,3,3],[0,1,3,3,3],[0,2,3,3,3],[0,1,3,0,3]]

num = 10
depweb2 = []

for i in range(0,num):
    new = []
    for j in range(0,num):
        new.append(random.randint(0,4))
    depweb2.append(new)

#print(depweb2)
symbolic_depWeb = Array('symbolic_depWeb', IntSort(), IntSort())

for i in range(len(depweb2)):
    for j in range(len(depweb2[0])):
        symbolic_depWeb = Store(symbolic_depWeb, len(depweb2)*i+j, depweb2[i][j])

set = findValidOrders(symbolic_depWeb,10,[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9]])
print(set)
set = findValidOrders(symbolic_depWeb,10,set)
print(set)

set = findValidOrders(symbolic_depWeb,10,set)
print(set)

set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)

print(set)
set = findValidOrders(symbolic_depWeb,10,set)
print(set)