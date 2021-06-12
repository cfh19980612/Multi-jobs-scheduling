import numpy as np
import time
def min_list(lt, D, machine_list, phyc_time):
  list_a = [[],[]]
  list_b = []
  a = 0
  b = 0
  min_time = 0 # save the value of min time 

  machine_list_copy = machine_list
  machine_list.sort()  
  #print(machine_list, phyc_time)
  while(a < D):
    #print(b, machine_list[b], phyc_time)
    # time.sleep(5)
    # print(b)
    list_a = [[],[]]
    b += 1
    a = 0

    if(phyc_time < machine_list[b]):
      phyc_time = machine_list[b]
    for i in range(len(machine_list_copy)):
      if(phyc_time >= machine_list_copy[i]):
        list_a[0].append(i)
        list_a[1].append(machine_list_copy[i] + lt[i])
        a += 1
        # print(list_a)

  # if(phyc_time == 0):
  #   list_a[0] = [i for i in range(len(machine_list))]
  #   list_a[1] = [0]*len(machine_list)
  #   for i in range(len(machine_list)):
  #     list_a[1].append(machine_list[i] + lt[i])

  for i in range(D):
    # print(min(list_a[1]))
    if phyc_time == 0:
      min_time = 0
    min_time = min(list_a[1])
    list_b.append(list_a[0][list_a[1].index(min_time)]) # one device choosed
    list_a[0].remove(list_a[0][list_a[1].index(min_time)])
    list_a[1].remove(min_time)
  # print(list_b)
  return list_b, phyc_time


def FIFO_solver(Jobs, Num_of_Machines):
  arrive_list = [] # record the arriving time of each job, and sort it
  machine_list = [0]*Num_of_Machines # the situation of machine
  time_list = []
  phyc_time = 0
  job_time = []
  max_time = 0
  
  for i in range(len(Jobs)):
    j=0
    if(Jobs[i].r > max_time or len(arrive_list) == 0 or Jobs[i].r == max_time):  # put the lately arriving jobs to the end of list or init the first jobs to the list
      arrive_list.append(Jobs[i])
      max_time = Jobs[i].r
    elif(Jobs[i].r < arrive_list[j].r ): # put the earlly arriving jobs to the head of list
      arrive_list.insert(0, Jobs[i])
    elif(Jobs[i].r == arrive_list[j].r):
      arrive_list.insert(j+1,Jobs[i])
    else:
      while(Jobs[i].r > arrive_list[j].r):  # put the arriving jobs to the middle of list
        if(Jobs[i].r < arrive_list[j+1].r):
          arrive_list.insert(j+1,Jobs[i])
          break
        if(Jobs[i].r == arrive_list[j+1].r):
          arrive_list.insert(j+2,Jobs[i])
          break
        j += 1
  for i in range(len(arrive_list)):
    time_list = []
    for j in range(len(machine_list)):
      time_list.append(arrive_list[i].t_c[j] + arrive_list[i].t_s[j])
    if(phyc_time < arrive_list[i].r):
      phyc_time = arrive_list[i].r
    choose_machine_list, phyc_time = min_list(time_list, arrive_list[i].D, machine_list, phyc_time)
    # print(choose_machine_list,phyc_time)
    for j in range(len(choose_machine_list)):
      machine_list[choose_machine_list[j]] = phyc_time + time_list[choose_machine_list[len(choose_machine_list)-1]]*arrive_list[i].B
    job_time.append(machine_list[choose_machine_list[0]])
  
  result = 0
  for i in range (len(Jobs)):
    result += job_time[i]*Jobs[i].weight
  return result
  #time