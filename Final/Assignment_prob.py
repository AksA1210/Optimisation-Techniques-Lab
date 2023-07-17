# -*- coding: utf-8 -*-
"""
Created on Mon May 22 22:04:46 2023

@author: user
"""

from ortools.linear_solver import pywraplp


def main():
    # Data
    print("\n\n------------------------ASSIGNMENT PROBLEM------------------------")
    print("\n")
    num_jobs = int(input("Enter the no: of jobs : "))
    num_operators = int(input("Enter the no: of machines : "))
    costs = []
    if(num_jobs == num_operators):
        for i in range(num_jobs):
            l = []
            print("Enter the values row by row : ")
            costs.append(l)
    else:
        print("Cannot proceed further as the no: of jobs is not equal to no: of machines.")
    '''costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100],
    ]
    num_operators = len(costs)
    num_jobs = len(costs[0])'''

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        return

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if worker i is assigned to task j.
    x = {}
    for i in range(num_operators):
        for j in range(num_jobs):
            x[i, j] = solver.IntVar(0, 1, '')

    # Constraints
    # Each worker is assigned to at most 1 task.
    for i in range(num_operators):
        solver.Add(solver.Sum([x[i, j] for j in range(num_jobs)]) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(num_jobs):
        solver.Add(solver.Sum([x[i, j] for i in range(num_operators)]) == 1)

    # Objective
    objective_terms = []
    for i in range(num_operators):
        for j in range(num_jobs):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n')
        for i in range(num_operators):
            for j in range(num_jobs):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    print(f'Worker {i} assigned to task {j}.' +
                          f' Cost: {costs[i][j]}')
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()
