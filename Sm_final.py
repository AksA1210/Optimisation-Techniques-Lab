# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:57:17 2023

@author: user
"""

import numpy
# import sys
def maximise():
     print("Checking if all inequalities are <=")
     
     
     
def minimise():
    print("Checking if all inequalities are >=")
     
     
         
         
def main():
    ch = 'y'
    while ch == 'y':
        print("\n\n---------------SIMPLEX METHOD---------------")
        print("\n\n-----------------Main Menu------------------")
        print("\n")
        print("1. INPUT THE PARAMETERS AND CONSTRAINTS")
        print("2. MAXIMISE")
        print("3. MINIMISE")
        print("4. EXIT")
        choice = int(input("Enter choice : "))
        if choice == 1:
            n = int(input("Enter the no: of variables : "))    
            m = int(input("Enter the no: of constraints : "))
            method = SimplexMethod()
            matrix = method.generateMatrix(n,m)
            for i in range(m):
                eq = ''
                print("\n---------------EQUATION",i+1,"-----------------\n")  
                for j in range(n):
                    print("Enter coeffecient number ",(j+1)," in the equation",(i+1))
                    eq+=input()+' , '
                print("\nChoose the inequality : ")
                print()
                print("1. LTE (<=)")
                print("2. GTE (>=)")
                print("3. EQUAL (=)")
                ineq=int(input())
                if ineq == 1:
                    eq +=' <= '
                elif ineq == 2:
                    eq +=' >= '
                elif ineq == 3:
                    eq +=' == '
                else:
                    break
                print("\nEnter inequality value(constant in the RHS)" )
                eq += input()
                print("\nconstraint",i+1," : " ,eq,end='\n')
                print()
                print("\n")
                method.constraint(matrix,eq)    
                #a = np.zeros((n+1,m+1))
                #cj = np.zeros((n+1))
        if choice == 2:
            print(method.maximization(matrix))
        elif choice == 3:
            print(method.minimization(matrix))
        elif choice == 4:
            print("Exiting out of the program.......")
            break 
        else:
            print("\nInvalid choice")
            break
    ch = input("\nDo you want to continue(y/n) ? : ")
    
class SimplexMethod:
    def generateMatrix(self,variables,constants):    
        table = numpy.zeros((constants+1, variables+constants+2))    
        return table


    def roundNextRow(self,t):    
        minim = min(t[:-1,-1])    
        if minim >= 0:        
            return False      
        return True

    def RoundNext(self,t):    
        lengthRow = len(t[:,0])  
        minim = min(t[lengthRow-1,:-1])    
        if minim >= 0:
            return False
        return True

    def locateaNegativeRows(self,t):
        lengthColumn = len(t[0,:])
        minim = min(t[:-1,lengthColumn-1])
        if minim<=0:        
            y = numpy.where(t[:-1,lengthColumn-1] == minim)[0][0]
        else:
            y = None
        return y

    def locateNegatives(self,t):
        lengthRow = len(t[:,0])
        minim = min(t[lengthRow-1,:-1])
        if minim<=0:
            z = numpy.where(t[lengthRow-1,:-1] == minim)[0][0]
        else:
            z = None
        return z

    def locatePivotR(self,t):
        to = []        
        r = self.locateaNegativeRows(t)
        row = t[r,:-1]
        minim = min(row)
        c = numpy.where(row == minim)[0][0]
        column = t[:-1,c]
        for x, y in zip(column,t[:-1,-1]):
            if x**2>0 and y/x>0:
                to.append(y/x)
            else:                
                to.append(15000)
        loc = to.index(min(to))        
        return [loc,c]

    def locatePivot(self,t):
        if self.RoundNext(t):
            allRecords = []
            negative = self.locateNegatives(t)
            for i,b in zip(t[:-1,negative],t[:-1,-1]):
                if b/i >0 and i**2>0:
                    allRecords.append(b/i)
                else:
                    allRecords.append(15000)
            loc = allRecords.index(min(allRecords))
            return [loc,negative]


    def pivot(self,row,col,matrix):
        lengthRow = len(matrix[:,0])
        lengthColumn = len(matrix[0,:])
        t = numpy.zeros((lengthRow,lengthColumn))
        pivotRow = matrix[row,:]
        if matrix[row,col]**2>0:
            e = 1/matrix[row,col]
            r = pivotRow*e
            for i in range(len(matrix[:,col])):
                k = matrix[i,:]
                c = matrix[i,col]
                if list(k) == list(pivotRow):
                    continue
                else:
                    t[i,:] = list(k-r*c)
            t[row,:] = list(r)
            return t
        else:
            print('Cannot pivot on this element.')

    def conversion(self,equation):
        equation = equation.split(',')
        if 'LTE' in equation:
            lte = equation.index('LTE')
            del equation[lte]
            equation = [float(a) for a in equation]
            return equation
        if 'GTE' in equation:
            gte = equation.index('GTE')
            del equation[gte]
            equation = [float(a)*-1 for a in equation]
            return equation

    def convertMinimum(self,t):
        t[-1,:-2] = [-1*a for a in t[-1,:-2]]
        t[-1,-1] = -1*t[-1,-1]    
        return t

    def generateVariable(self,t):
        lengthColumn = len(t[0,:])
        lengthRow = len(t[:,0])
        va = lengthColumn - lengthRow -1
        variables = []
        for w in range(va):
            variables.append('x'+str(w+1))
        return variables

    def addConstants(self,t):
        lengthRow = len(t[:,0])
        e = []
        for i in range(lengthRow):
            to = 0
            for q in t[i,:]:                      
                to += q**2
            if to == 0:
                e.append(to)
        if len(e) > 1:
            return True
        return False

    def constraint(self,t,equation):
        if self.addConstants(t) == True:
            lengthColumn = len(t[0,:])
            lengthRow = len(t[:,0])
            v = lengthColumn - lengthRow -1      
            k = 0
            while k < lengthRow:            
                checkRow = t[k,:]
                to = 0
                for b in checkRow:
                    to += float(b**2)
                if to == 0:                
                    row = checkRow
                    break
                k +=1
            equation = self.conversion(equation)
            d = 0
            while d<(len(equation)-1):
                row[d] = equation[d]
                d += 1        
            row[-1] = equation[-1]
            row[v+k] = 1    
        else:
            print('Constraint Not Added.')

    def objectiveAdd(self,t):
        lengthRow = len(t[:,0])
        e = []
        for x in range(lengthRow):
            to = 0        
            for y in t[x,:]:
                to += y**2
            if to == 0:
                e.append(to)    
        if len(e)!=1:
            return False
        return True

    def objective(self,t,equation):
        if self.objectiveAdd(t)==True:
            equation = [float(n) for n in equation.split(',')]
            lengthRow = len(t[:,0])
            row = t[lengthRow-1,:]
            a = 0        
            while a<len(equation)-1:
                row[a] = equation[a]*-1
                a += 1
            row[-2] = 1
            row[-1] = equation[-1]
        else:
            print('Add constraints before adding objective function.')

    def maximization(self,t):
        while self.roundNextRow(t)==True:
            t = self.pivot(self.locatePivotR(t)[0],self.locatePivotR(t)[1],t)
        while self.RoundNext(t)==True:
            t = self.pivot(self.locatePivot(t)[0],self.locatePivot(t)[1],t)        
        lengthColumn = len(t[0,:])
        lengthRow = len(t[:,0])
        var = lengthColumn - lengthRow -1
        x = 0
        valu = {}
        for x in range(var):
            column = t[:,x]
            su = sum(column)
            m = max(column)
            if float(su) == float(m):
                loc = numpy.where(column == m)[0][0]            
                valu[self.generateVariable(t)[x]] = t[loc,-1]
            else:
                valu[self.generateVariable(t)[x]] = 0
        valu['Maximum'] = t[-1,-1]
        return valu

    def minimization(self,t):
        t = self.convertMinimum(t)
        while self.roundNextRow(t) == True:
            t = self.pivot(self.locatePivotR(t)[0],self.locatePivotR(t)[1],t)    
        while self.RoundNext(t) == True:
            t = self.pivot(self.locatePivot(t)[0],self.locatePivot(t)[1],t)      
        lengthColumn = len(t[0,:])
        lengthRow = len(t[:,0])
        var = lengthColumn - lengthRow -1
        x = 0
        val = {}
        for x in range(var):
            column = t[:,x]
            su = sum(column)
            m = max(column)
            if float(su) == float(m):
                loc = numpy.where(column == m)[0][0]            
                val[self.generateVariable(t)[x]] = t[loc,-1]
            else:
                val[self.generateVariable(t)[x]] = 0
                val['Minimum'] = t[-1,-1]*-1
        return val
   

if __name__ == "__main__":
     main()    

    
