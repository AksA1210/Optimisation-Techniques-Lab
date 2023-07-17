# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:46:32 2023

@author: user
"""

class Scheduling:

  def schedule(self, n, deadline, jobs):
    self.fdeadline = deadline
    self.J = []
    self.J.append(jobs[0])
    self.i = 1
    while self.i <= n:
      self.K = self.J.copy() 
      self.K.append(jobs[self.i]) 
      self.i = self.i + 1
      if self.feasible(self.K, self.fdeadline) == True :
        self.J = self.K

    return self.J  

  def feasible(self, K, fdl):
    self.tmp = K
    self.isFeasible = True

    self.i = 0
    self.j = 1
    self.k = 0 

    while self.i < len(self.tmp):
      while self.j < len(self.tmp):
        self.index1 = self.i
        self.index2 = self.j
        if (fdl[self.index1] > fdl[self.index2]):
          self.tmp[i], self.tmp[j]  =  self.tmp[j], self.tmp[i]  

    while self.k < len(self.tmp):
       self.job  = self.tmp[self.k]
       if (fdl[self.job] < k + 1):
         isFeasible = False
         break

    return isFeasible 


def main():
   sins = Scheduling()
   n = 4
   deadline = [1,1,2,2]
   jobs = [4, 2, 1, 3]
   sjobs = sins.schedule(n, deadline, jobs)
   print (sjobs)  

if __name__ == "__main__":
  main()