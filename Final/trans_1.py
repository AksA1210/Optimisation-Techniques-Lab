# -*- coding: utf-8 -*-
"""
Created on Sun May  7 22:59:49 2023

@author: user
"""
# Prg 1

import numpy as np
def get_balanced(supply, demand, costs, penalties = None):
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    if total_supply < total_demand:
        if penalties is None:
            raise Exception('Supply less than demand, penalties required')
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [penalties]
        return new_supply, demand, new_costs
    if total_supply > total_demand:
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs + [[0 for _ in demand]]
        return supply, new_demand, new_costs
    return supply, demand, costs
def vogel(supply, demand,costs):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    m=len(supply)
    n=len(demand)
    i = 0
    j = 0
    bfs = []
    while len(bfs) < len(supply) + len(demand) - 1:
        s = supply_copy[i]
        d = demand_copy[j]
        v = min(s, d)
        supply_copy[i] -= v
        demand_copy[j] -= v
        bfs.append(((i, j), v))
        if supply_copy[i] == 0 and i < len(supply) - 1:
            i += 1
        elif demand_copy[j] == 0 and j < len(demand) - 1:
            j += 1
    cost = 0
    bfs_arr = [[0 for i in range(n)] for j in range(m)] 
    for item in bfs:
        bfs_arr[item[0][0]][item[0][1]]=item[1]
    print('\n The initial table is :\n',bfs_arr)
    for item in bfs:
        cost=cost+costs[item[0][0]][item[0][1]]*item[1]
    print('\nTotal cost is : ',cost)
    return bfs
def get_us_and_vs(bfs, costs):
    us = [None] * len(costs)
    vs = [None] * len(costs[0])
    us[0] = 0
    bfs_copy = bfs.copy()
    while len(bfs_copy) > 0:
        for index, bv in enumerate(bfs_copy):
            i, j = bv[0]
            if us[i] is None and vs[j] is None: continue
                
            cost = costs[i][j]
            if us[i] is None:
                us[i] = cost - vs[j]
            else: 
                vs[j] = cost - us[i]
            bfs_copy.pop(index)
            break
            
    return us, vs
def get_ws(bfs, costs, us, vs):
    ws = []
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
            if non_basic:
                ws.append(((i, j), us[i] + vs[j] - cost))
    
    return ws
def can_be_improved(ws):
    for p, v in ws:
        if v > 0: return True
    return False
def get_entering_variable_position(ws):
    ws_copy = ws.copy()
    ws_copy.sort(key=lambda w: w[1])
    return ws_copy[-1][0]
def get_possible_next_nodes(loop, not_visited):
    last_node = loop[-1]
    nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
    if len(loop) < 2:
        return nodes_in_row + nodes_in_column
    else:
        prev_node = loop[-2]
        row_move = prev_node[0] == last_node[0]
        if row_move: return nodes_in_column
        return nodes_in_row
def get_loop(bv_positions, ev_position):
    def inner(loop):
        if len(loop) > 3:
            can_be_closed = len(get_possible_next_nodes(loop, [ev_position])) == 1
            if can_be_closed: return loop
        
        not_visited = list(set(bv_positions) - set(loop))
        possible_next_nodes = get_possible_next_nodes(loop, not_visited)
        for next_node in possible_next_nodes:
            new_loop = inner(loop + [next_node])
            if new_loop: return new_loop
    
    return inner([ev_position])
def loop_pivoting(bfs, loop):
    even_cells = loop[0::2]
    odd_cells = loop[1::2]
    get_bv = lambda pos: next(v for p, v in bfs if p == pos)
    leaving_position = sorted(odd_cells, key=get_bv)[0]
    leaving_value = get_bv(leaving_position)
    
    new_bfs = []
    for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]:
        if p in even_cells:
            v += leaving_value
        elif p in odd_cells:
            v -= leaving_value
        new_bfs.append((p, v))
        
    return new_bfs
def transportation_method(supply, demand, costs, penalties = None):
    balanced_supply, balanced_demand, balanced_costs = get_balanced(
        supply, demand, costs
    )
    def inner(bfs):
        us, vs = get_us_and_vs(bfs, balanced_costs)
        ws = get_ws(bfs, balanced_costs, us, vs)
        if can_be_improved(ws):
            ev_position = get_entering_variable_position(ws)
            loop = get_loop([p for p, v in bfs], ev_position)
            return inner(loop_pivoting(bfs, loop))
        return bfs
    
    basic_variables = inner(vogel(balanced_supply, balanced_demand,costs))
    ans = np.zeros((len(costs), len(costs[0])))
    for (i, j), v in basic_variables:
        ans[i][j] = int(v)

    return ans
def get_total_cost(costs, ans):
    total_cost = 0
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            total_cost += cost * ans[i][j]
    return total_cost
print("\n-------------TRANSPORTATION PROBLEM-----------------")
m = int(input("Enter no: of rows : "))
n = int(input("Enter no: of columns : "))
print("\nEnter all costs in one line : ")
entries = list(map(int, input().split()))  
costs = np.array(entries).reshape(m, n)
print('\n The costs are : \n',costs)
print('\n')
supply = list(map(int,input("Enter the supply values : ").strip().split()))[:m]
demand = list(map(int,input("Enter the demand values : ").strip().split()))[:n]
print('\n')
ans = transportation_method(supply, demand, costs)
print('\n')
print('\n The optimal solution is : \n',ans)
print()
print('\n')
print('Total optimal cost : ', get_total_cost(costs, ans))
'''Enter m:3
Enter n:4
Enter all costs in one line
2 2 2 1 10 8 5 4 7 6 6 8

 The costs are:
 [[ 2  2  2  1]
 [10  8  5  4]
 [ 7  6  6  8]]


Enter the supply values : 30 70 50


Enter the demand values : 40 30 40 40



 The initial bfs is:
 [[30, 0, 0, 0], [10, 30, 30, 0], [0, 0, 10, 40]]
total bfs cost is:  930



 The optimal solution is:
 [[30.  0.  0.  0.]
 [ 0.  0. 30. 40.]
 [10. 30. 10.  0.]]
total optimal cost:  680.0'''
 