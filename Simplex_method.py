# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:55:01 2023

@author: user
"""

import numpy as np
#from fractions import Fraction
print("\n\n----------SIMPLEX ALGORTITHM----------\n\n")
# A will store the coefficient of the constraints
'''A = np.array([[1,1,0,1],[2,1,1,0]])
# b will store the amount of resources
b = np.array([8,10])
# C will contain the coefficients of objective function z
C = np.array([1,1,0,0])
print(A)
print(b)
print(C) '''
S = np.array([[-1,1,1,0,0,11],[1,1,0,1,0,27],[2,5,0,0,1,90],[-4,-6,0,0,0,0]])
print(S)
print("\n\n--------------------------------------")
print("\n")
column = S[-1,:]
a = min(column)
print(a)
print("\nThe column with the element",a,"is chosen")
# i.e the 2nd column
def find(a, S):
    for i in range(len(S)):
        for j in range(len(S[i])):
            if S[i][j] == a:
                return (i+1, j+1)
CC = find(a, S) 
CC = list(CC)
print("\nThe chosen column no is : ",CC[1])
# Row to be chosen based upon the minimum ratio
ratio = []
ratio1 = S[0][5]/S[0][1]
ratio.append(ratio1)
ratio2 = S[1][5]/S[1][1]
ratio.append(ratio2)
ratio3 = S[2][5]/S[2][1]
ratio.append(ratio3)
#ratio.append(ratio1,ratio2,ratio3)
min_ratio = min(ratio)
print(ratio)
print("\nMinimum ratio is : ",min_ratio)
# row to be chosen is row 1
row = S[ :,5 ]
CR = find(min_ratio , S)
CR = list(CR)

print(row)
print("\nThe chosen row no is : ",CR[0])

# Pivot element to be chosen
# pivot = S[0][1]
pivot = S[CR[0]-1,CC[1]-1]
print("\nPivot element : ",pivot)

# Has to make all the elements just below the pivot element as 0

print("The chosen column no is : ",CC[1])
print()
# Row operation : R2 -> R2 - R1
#for i in range(1,2):
for j in range(0,6):
    S[1][j] = S[1][j] - S[0][j]
print(S)
print()
# Row operation : R3 -> R3 - 5R1

#for i in range(1,2):
for j in range(0,6):
    S[2][j] = S[2][j] - 5*S[0][j]
print(S)
print()
# Row operation : R4 -> R4 + 6R1

#for i in range(1,2):
for j in range(0,6):
    S[3][j] = S[3][j] + 6*S[0][j]
print(S)
print()
# Relative profit = Cj- zj

