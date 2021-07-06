import gurobipy as gp
import numpy as np

from gurobipy import GRB
from Job_Environment import *
from Task_Environment import *

def make_Matrix(Jobs, Num_of_Jobs, Num_of_Machines):
  P = [[] for i in range(Num_of_Jobs)]
  Q = [[] for i in range(Num_of_Jobs)]
  for i in range(Num_of_Jobs):
    for j in range(Num_of_Machines):
      P[i].append((Jobs[i].t_c[j] * Jobs[i].D + Jobs[i].t_s[j])*Jobs[i].I)
  # print(P)
  for i in range(Num_of_Jobs):
    for j in range(Num_of_Machines):
      for k in range(Num_of_Jobs):
        Q[i].append((1 + k)*P[i][j])
  # print(Q)
  return P,Q

def add_r(P, Jobs, Q, choose_machine_list, Num_of_Jobs, Num_of_Machines):
  machine_list = [0 for a in range(Num_of_Machines)]
  machine_Time = [{} for i in range(Num_of_Machines)]
  time = 0

  jobs_time = [0 for i in range(len(Jobs))]

  for i in range(Num_of_Machines):
    for j in range(Num_of_Jobs):
      for k in range(Num_of_Machines * Num_of_Jobs):
        if(choose_machine_list[j, k] == 1):
          a = (k + 1) / Num_of_Jobs
          b = (k + 1) % Num_of_Jobs
          if(b != 0):
            machine_Time[int(a)][int(b)] = j
          if(b == 0):
            machine_Time[int(a - 1)][Num_of_Jobs] = j
  # print(machine_Time)
  for i in range(Num_of_Machines):
    for j in range(len(machine_Time[i])):
      # print(machine_Time[i][len(machine_Time[i]) - j])
      if(Jobs[machine_Time[i][len(machine_Time[i]) - j]].r > machine_list[i]):
        machine_list[i] = Jobs[machine_Time[i][len(machine_Time[i]) - j]].r + P[machine_Time[i][len(machine_Time[i]) - j]][i]
        jobs_time[machine_Time[i][len(machine_Time[i]) - j]] = machine_list[i]
        time += machine_list[i] * Jobs[machine_Time[i][len(machine_Time[i]) - j]].weight
      else:
        # print(len(machine_list))
        machine_list[i] = machine_list[i] + P[machine_Time[i][len(machine_Time[i]) - j]][i]
        jobs_time[machine_Time[i][len(machine_Time[i]) - j]] = machine_list[i]
        time += machine_list[i] * Jobs[machine_Time[i][len(machine_Time[i]) - j]].weight
  # print(jobs_time, time)
  return jobs_time, time
def Allox_Solver(Jobs, Num_of_Jobs, Num_of_Machines):
  try:
    P,Q = make_Matrix(Jobs, Num_of_Jobs, Num_of_Machines)
    # Create a new model
    m = gp.Model("DRF")
    m.setParam('OutputFlag', 0)

    # Create variables
    choose_machine_list = m.addVars(Num_of_Jobs, Num_of_Machines*Num_of_Jobs, vtype = GRB.BINARY)
    C = m.addVars(Num_of_Jobs, vtype = GRB.CONTINUOUS)

    # object
    m.setObjective(C.sum('*') , GRB.MINIMIZE)

    # constraint 1: one job one line
    m.addConstrs((choose_machine_list.sum(i,'*') == 1 for i in range(Num_of_Jobs)),"constraint-1")
    # constraint 1: one gpu each time one line
    m.addConstrs((choose_machine_list.sum('*',j) <= 1 for j in range(Num_of_Jobs*Num_of_Machines)),"constraint-2")

    # constraint 2: value of C
    m.addConstrs((C[i] == gp.quicksum(choose_machine_list[i,j]*Q[i][j] for j in range(Num_of_Jobs*Num_of_Machines)) for i in range(Num_of_Jobs) ),"constraint-3")

    # Optimize model
    m.optimize()
    m.update()
    m.write("test.lp")
    if m.status == GRB.OPTIMAL:
        # print(1)
        list_r = m.getAttr('x', choose_machine_list)
        # print(list_r)
        # print(m.getAttr('x', C))
    # print(choose_machine_list,C)
    return add_r(P, Jobs, Q, list_r,Num_of_Jobs, Num_of_Machines)
    # return m.objVal

  except gp.GurobiError as e:
      print('Error code ' + str(e.errno) + ': ' + str(e))

  except AttributeError:
      print('Encountered an attribute error')