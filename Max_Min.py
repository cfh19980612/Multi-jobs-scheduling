from __future__ import division
import numpy as np
import gurobipy as gp
import numpy as np
from gurobipy import GRB
from Job_Environment import *
import time
import math
choose_jobs = 10

def add(r_sort_list):
  next_turn_machine_list = []
  if(len(r_sort_list) > choose_jobs):
    for i in range(choose_jobs):
      next_turn_machine_list.append(r_sort_list[0])
      r_sort_list.pop(0)
  else:
    for i in range(len(r_sort_list)):
      next_turn_machine_list.append(r_sort_list[0])
      r_sort_list.pop(0)
  return next_turn_machine_list, r_sort_list
def add_weight(job_machine_list_bin, weight_sort_list,Jobs):
  total_weight = 0
  for i in range(len(job_machine_list_bin)):
    if(job_machine_list_bin[weight_sort_list[i]] != 1):
      total_weight += Jobs[weight_sort_list[i]].weight
  return total_weight
def intl_machine_list(weight_sort_list, next_turn_machine_list, job_machine_list, job_machine_list_bin, r_sort_list):
  decimal = 0
  job_machine_list_copy = [0 for i in range(len(job_machine_list))]
  for i in range(len(next_turn_machine_list)):
    job_machine_list_copy[i] = math.modf(job_machine_list[i])[1]
    decimal += math.modf(job_machine_list[i])[0]
  #max_value = 0
  #a = [1.4337008678894936, 1.4346333998772935, 0.08430142396008186, 0.8626844743899631, 1.0989067940695187, 8.94293606032624, 1.4000125790791906, 1.5626334141111398, 0.2821231483200846, 1.0072681739118214, 1.2127076589654007, 0.4217175078320351, 0.7059404866027967, 0.6553140522276847, 0.49595261983162375, 0.6560160217493896, 1.2010023723134733, 0.5650671005959285, 0.47352534025836235, 2.2203130518858516]
  # for i in range(len(a)):
  #   max_value += a[i]
  #print('max_value',max_value, job_machine_list_copy)
  for i in range(len(next_turn_machine_list)):
    # print(decimal)
    job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]] = int(job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]])
    if(decimal >= 0.9):
      job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]] += 1
      decimal -= 1
      job_machine_list_bin[weight_sort_list[len(next_turn_machine_list) - i - 1]] = 1
    else:
      if(job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]] < 0.9):
        job_machine_list_bin[weight_sort_list[len(next_turn_machine_list) - i - 1]] = 0
        job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]] = 0
      if(job_machine_list_bin[weight_sort_list[len(next_turn_machine_list) - i - 1]] == 0):
        if(job_machine_list_copy[weight_sort_list[len(next_turn_machine_list) - i - 1]] == 0):
          r_sort_list.insert(0, next_turn_machine_list[weight_sort_list[len(next_turn_machine_list) - i - 1]])
        else:
          job_machine_list_bin[weight_sort_list[len(next_turn_machine_list) - i - 1]] = 1
  # print(job_machine_list_copy, job_machine_list_bin, r_sort_list)
  return job_machine_list_copy, job_machine_list_bin, r_sort_list
def divide_Machine_to_Job(Jobs, Num_of_Jobs, Num_of_Machines):
  total_time = 0
  r_sort_list = []
  max_r = 0
  for i in range(Num_of_Jobs):
    #print(Jobs[i].r, max_r)
    if(Jobs[i].r >= max_r):
      max_r = Jobs[i].r
      r_sort_list.append(i)
    else:
      for j in range(len(r_sort_list)):
        if(Jobs[i].r <= Jobs[r_sort_list[j]].r):
          r_sort_list.insert(j, i)
          break
        # print(Jobs[i].r,r_sort_list[j],r_sort_list)
        # r_sort_list.insert(0, i)
  # print(r_sort_list)
  next_turn_machine_list = []
  machine_free_time = 0
  while(len(r_sort_list) != 0):

    next_turn_machine_list,r_sort_list = add(r_sort_list)

    max_weight = total_weight = 0
    weight_sort_list = []
    current_num_of_machine = Num_of_Machines
    job_machine_list = [0 for i in range(len(next_turn_machine_list))]
    job_machine_list_bin = [0 for i in range(len(next_turn_machine_list))]
    
    for i in range(len(next_turn_machine_list)):
      # print(Jobs[next_turn_machine_list[i]].weight, max_weight)
      if(Jobs[next_turn_machine_list[i]].weight >= max_weight):
        max_weight = Jobs[next_turn_machine_list[i]].weight
        weight_sort_list.append(i)
      else:
        for j in range(len(weight_sort_list)):
          if(Jobs[next_turn_machine_list[i]].weight <= Jobs[next_turn_machine_list[weight_sort_list[j]]].weight):
            # print(next_turn_machine_list, weight_sort_list)
            weight_sort_list.insert(j, i)
            break
      total_weight += Jobs[i].weight
    # print(next_turn_machine_list, weight_sort_list)
    while(current_num_of_machine != 0):
      # total_weight = add_weight(job_machine_list_bin, weight_sort_list, Jobs)
      # time.sleep(0.5)
      for i in range(len(next_turn_machine_list)):
        # time.sleep(0.5)
        # print(current_num_of_machine)
        # print(next_turn_machine_list, r_sort_list, weight_sort_list, job_machine_list_bin, job_machine_list, Jobs[i].weight, total_weight, current_num_of_machine)
        # if(job_machine_list_bin[weight_sort_list[i]] == 0):
          # print(current_num_of_machine*(Jobs[weight_sort_list[i]].weight/total_weight))
        if(current_num_of_machine*(Jobs[weight_sort_list[i]].weight/total_weight) + job_machine_list[weight_sort_list[i]] < Jobs[weight_sort_list[i]].D):
          job_machine_list[weight_sort_list[i]] += current_num_of_machine*(Jobs[weight_sort_list[i]].weight/total_weight)
          # print(current_num_of_machine)
          current_num_of_machine -= current_num_of_machine*(Jobs[weight_sort_list[i]].weight/total_weight)
          if(current_num_of_machine != 0 and i == len(next_turn_machine_list) - 1):
            current_num_of_machine = 0
          # print(current_num_of_machine)
          # total_weight -= Jobs[weight_sort_list[i]].weight
          # if(current_num_of_machine < 0.1): 
          #   for i in range(len(next_turn_machine_list)):
          #     if(job_machine_list[weight_sort_list[i]] > 0.5):job_machine_list_bin[weight_sort_list[i]] = 1
          #     else: job_machine_list_bin[weight_sort_list[i]] = 0
          #   current_num_of_machine = 0
          #   total_weight = 0
        else:
          # job_machine_list_bin[weight_sort_list[i]] = 1
          total_weight = add_weight(job_machine_list_bin, weight_sort_list, Jobs)
          current_num_of_machine -= Jobs[weight_sort_list[i]].D - job_machine_list[weight_sort_list[i]]
          # print(current_num_of_machine)
          job_machine_list[weight_sort_list[i]] = Jobs[weight_sort_list[i]].D
          # if(current_num_of_machine < 0.1): current_num_of_machine = 0
          job_machine_list_bin[weight_sort_list[i]] = 1
      for i in range(len(next_turn_machine_list)):
        # print(job_machine_list_bin[weight_sort_list[i]], current_num_of_machine)
        if(job_machine_list_bin[weight_sort_list[i]] != 1):
          if(current_num_of_machine > Jobs[weight_sort_list[i]].D - job_machine_list[weight_sort_list[i]]):
            current_num_of_machine -= Jobs[weight_sort_list[i]].D - job_machine_list[weight_sort_list[i]]
            # print(current_num_of_machine)
            job_machine_list_bin[weight_sort_list[i]] = 1
          else:
            job_machine_list[weight_sort_list[i]] += current_num_of_machine
            job_machine_list_bin[weight_sort_list[i]] = 1
            current_num_of_machine = 0
            break
        if(current_num_of_machine != 0 and i == len(next_turn_machine_list) - 1):
          current_num_of_machine = 0
    # print(next_turn_machine_list, r_sort_list, job_machine_list_bin, job_machine_list, current_num_of_machine)

    job_machine_list, job_machine_list_bin, r_sort_list = intl_machine_list(weight_sort_list, next_turn_machine_list, job_machine_list, job_machine_list_bin, r_sort_list)
    # print(machine_free_time)
    # print(next_turn_machine_list, job_machine_list, job_machine_list_bin,r_sort_list, Num_of_Machines)
    machine_free_time, total_time_copy = gurobi(machine_free_time, next_turn_machine_list, job_machine_list, Jobs, Num_of_Machines)
    # print(machine_free_time)
    total_time += total_time_copy
  # print(total_time)
  return total_time

def gurobi(machine_free_time, next_turn_machine_list, job_machine_list, Jobs,  Num_of_Machines):
  #print(machine_free_time)
  try:
    max_time_1 = 0.0
    if(job_machine_list.count(0) != 0):
      for i in range(job_machine_list.count(0)):
        #print(job_machine_list.index(0))
        next_turn_machine_list.pop(job_machine_list.index(0))
        job_machine_list.remove(0)
    job_machine_list_copy = [0 for i in range(len(job_machine_list))]
    job_machine_list_remaining = [0 for i in range(len(job_machine_list))]
    for i in range(len(next_turn_machine_list)):
      if(job_machine_list[i] == 0): 
        job_machine_list_copy[i] = 0
        job_machine_list_remaining[i] = job_machine_list[i]
      else: 
        job_machine_list_copy[i] = int(Jobs[next_turn_machine_list[i]].D/job_machine_list[i])
        # print(int(Jobs[next_turn_machine_list[i]].D/job_machine_list[i]))
        if(Jobs[next_turn_machine_list[i]].D % job_machine_list[i] != 0):
          # print(Jobs[next_turn_machine_list[i]].D % job_machine_list[i])
          job_machine_list_remaining[i] = Jobs[next_turn_machine_list[i]].D % job_machine_list[i]
          # job_machine_list_copy[i] += 1
        else: job_machine_list_remaining[i] = 0
    # Create a new model
    m = gp.Model("minmax")
    m.setParam('OutputFlag', 0)
    # print(job_machine_list_copy,job_machine_list,job_machine_list_remaining,next_turn_machine_list)
    # Create variables
    choose_machine_list = m.addVars(len(next_turn_machine_list), Num_of_Machines, vtype = GRB.BINARY)
    choose_machine_list_copy = m.addVars(len(next_turn_machine_list), Num_of_Machines, vtype = GRB.BINARY)
    machine_or_r = m.addVars(len(next_turn_machine_list), vtype = GRB.BINARY)
    machine_or_r_1 = m.addVars(len(next_turn_machine_list), vtype = GRB.BINARY)
    C = m.addVars(len(next_turn_machine_list), Num_of_Machines, vtype = GRB.CONTINUOUS)
    C_MAX = m.addVars(len(next_turn_machine_list), Num_of_Machines, vtype = GRB.CONTINUOUS)
    C_MAX_REAL = m.addVars(len(next_turn_machine_list), vtype = GRB.CONTINUOUS)
    # object
    m.setObjective(gp.quicksum(Jobs[next_turn_machine_list[i]].weight*C_MAX_REAL[i] for i in range(len(next_turn_machine_list))), GRB.MINIMIZE)
    # constraint 1: one job one line
    m.addConstrs((choose_machine_list.sum(i,'*') == job_machine_list[i] for i in range(len(next_turn_machine_list))),"constraint-1")
    # m.addConstrs(((choose_machine_list_copy[i,j] == choose_machine_list[i,j] for i in range(len(next_turn_machine_list))
    #                                                                        for j in range(Num_of_Machines) if job_machine_list_remaining[i] == job_machine_list[i])),"constraint-2")
    m.addConstrs(((choose_machine_list_copy.sum(i,'*') == job_machine_list_remaining[i] for i in range(len(next_turn_machine_list)))),"constraint-3")
    m.addConstrs(((choose_machine_list_copy[i,j] - choose_machine_list[i,j] <= 0 for i in range(len(next_turn_machine_list)) for j in range(Num_of_Machines) if job_machine_list_remaining[i] != 0)),"constraint-4")
    # m.addConstrs(((choose_machine_list_copy[i,j] != 1 for i in range(len(next_turn_machine_list)) for j in range(Num_of_Machines) if int(Jobs[i].D%job_machine_list[i]) != 0)),"constraint-4")
    # constraint 2: one gpu each time one line
    m.addConstrs((choose_machine_list.sum('*',j) <= 1 for j in range(Num_of_Machines)),"constraint-5")
    m.addConstrs((choose_machine_list_copy.sum('*',j) <= 1 for j in range(Num_of_Machines)),"constraint-6")
    # constraint 3: value of C
    m.addConstrs((C[i,j] == (choose_machine_list[i,j]*(machine_or_r[i]*machine_free_time + machine_or_r_1[i]*Jobs[next_turn_machine_list[i]].r + (Jobs[next_turn_machine_list[i]].t_s[j]+Jobs[next_turn_machine_list[i]].t_c[j]*int(Jobs[next_turn_machine_list[i]].D/job_machine_list[i]))*Jobs[next_turn_machine_list[i]].E*Jobs[next_turn_machine_list[i]].B)) for j in range(Num_of_Machines) for i in range(len(next_turn_machine_list)) ),"constraint-7-(1)")
    m.addConstrs((C_MAX[i,j] == C[i,j] + (choose_machine_list_copy[i,j]*Jobs[next_turn_machine_list[i]].t_c[j]*Jobs[next_turn_machine_list[i]].E*Jobs[next_turn_machine_list[i]].B)  for j in range(Num_of_Machines) for i in range(len(next_turn_machine_list))  if job_machine_list_remaining[i] != 0),"constraint-8")
    m.addConstrs((C_MAX[i,j] == C[i,j]  for j in range(Num_of_Machines) for i in range(len(next_turn_machine_list))  if job_machine_list_remaining[i] == 0),"constraint-8-(1)")
    # constraint 4:
    m.addConstrs((C_MAX_REAL[i] >= C_MAX[i,j] for j in range(Num_of_Machines) for i in range(len(next_turn_machine_list))),"constraint-9")
    m.addConstrs((machine_or_r[i] == 1 for i in range(len(next_turn_machine_list)) if machine_free_time > Jobs[next_turn_machine_list[i]].r  ), "constraint-10")
    m.addConstrs((machine_or_r_1[i] == 1 for i in range(len(next_turn_machine_list)) if machine_free_time <= Jobs[next_turn_machine_list[i]].r), "constraint-11")
    # Optimize model
    m.optimize()
    m.update()
    m.write("test.lp")
    if m.status == GRB.OPTIMAL:
        # print(1)
        # max_time = 0
        # max_time_number = 0
        list_r = m.getAttr('x', C_MAX_REAL)
        # print(list_r)
        for i in range(len(list_r)):
          # print(type(list_r[i]))
          if(list_r[i] >= max_time_1):
            # max_time_number = i
            max_time_1 = list_r[i]
        # print(m.getAttr('x', C))
        # print(m.getAttr('x', C_MAX))
        # print(m.getAttr('x', C_MAX_REAL))
    else:
      if(machine_free_time > Jobs[next_turn_machine_list[i]].r):
        max_time_1 = Jobs[next_turn_machine_list[0]].weight*((machine_free_time + (Jobs[next_turn_machine_list[0]].t_s[0]+Jobs[next_turn_machine_list[0]].t_c[0]*job_machine_list_copy[0])*Jobs[next_turn_machine_list[0]].E*Jobs[next_turn_machine_list[0]].B))
        max_time_2 = ((machine_free_time + (Jobs[next_turn_machine_list[0]].t_s[0]+Jobs[next_turn_machine_list[0]].t_c[0]*job_machine_list_copy[0])*Jobs[next_turn_machine_list[0]].E*Jobs[next_turn_machine_list[0]].B))
      else:
        max_time_1 = Jobs[next_turn_machine_list[0]].weight*((Jobs[next_turn_machine_list[0]].r + (Jobs[next_turn_machine_list[0]].t_s[0]+Jobs[next_turn_machine_list[0]].t_c[0]*job_machine_list_copy[0])*Jobs[next_turn_machine_list[0]].E*Jobs[next_turn_machine_list[0]].B))
        max_time_2 = ((Jobs[next_turn_machine_list[0]].r + (Jobs[next_turn_machine_list[0]].t_s[0]+Jobs[next_turn_machine_list[0]].t_c[0]*job_machine_list_copy[0])*Jobs[next_turn_machine_list[0]].E*Jobs[next_turn_machine_list[0]].B))
      return max_time_1, max_time_2
    # print(max_time_1, m.objVal)
    return max_time_1, m.objVal
    # return m.objVal

  except gp.GurobiError as e:
      print('Error code ' + str(e.errno) + ': ' + str(e))

  except AttributeError:
      print('Encountered an attribute error')

def maxmin(Jobs, Num_of_Jobs, Num_of_Machines):
  result = divide_Machine_to_Job(Jobs, Num_of_Jobs, Num_of_Machines)
  return result 