import numpy as np
import math
from LP import *
from Job_Environment import *
from Task_Environment import *


def DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp):

    DREAM_result = [0 for i in range (Num_of_Jobs)]
    Idle_time = [0 for i in range (Num_of_Machines)]  # initial the idle time for each machine

    # generate pi
    # Step 1: Compute the middle computation finish time
    for i in range (Num_of_Jobs):
        for j in range (Jobs[i].I):
            for k in range (Jobs[i].D):
                Jobs[i].Tasks[j][k].Middle_time = x_lp[i][j][k] + max(Jobs[i].t_c)/2
    # Step 2: Sort tasks according their middle computation finish time
    All_tasks = []
    for i in range (Num_of_Jobs):
        for j in range (Jobs[i].I):
            for k in range (Jobs[i].D):
                All_tasks.append(Jobs[i].Tasks[j][k])
    All_tasks.sort(key=lambda x: x.Middle_time)
    
    # allocate resource for each task
    for t in range (len(All_tasks)):
        limite_time = 0  # initial the limited time according the previous iteration
        if All_tasks[t].iter_id == 0:
            limite_time = Jobs[All_tasks[t].job_id].r
        elif All_tasks[t].iter_id > 0:
            Previous_task = [0 for i in range (Jobs[All_tasks[t].job_id].D)]  # the finish time of tasks in the previous itertation
            for j in range (Jobs[All_tasks[t].job_id].D):
                Previous_task[j] = All_tasks[t].Real_Start + Jobs[All_tasks[t].job_id].Tasks[All_tasks[t].iter_id - 1][j].t_c[Jobs[All_tasks[t].job_id].Tasks[All_tasks[t].iter_id - 1][j].Real_Allocate]\
                    + Jobs[All_tasks[t].job_id].Tasks[All_tasks[t].iter_id - 1][j].t_s[Jobs[All_tasks[t].job_id].Tasks[All_tasks[t].iter_id - 1][j].Real_Allocate]
                limite_time = max(Previous_task)
        # compute the completion time for i task on each machine
        Time = [0 for m in range (Num_of_Machines)]
        for m in range (Num_of_Machines):
            Time[m] = max(Idle_time[m], limite_time) + All_tasks[t].t_c[m] + All_tasks[t].t_s[m]
        # search the machine
        M_r = Time.index(min(Time))

        # allocate M_* to i
        All_tasks[t].Real_Allocate = M_r
        # Need to change P ???

        # Result
        All_tasks[t].Real_Start = max(Idle_time[m], limite_time)
        All_tasks[t].Real_Complete = All_tasks[t].Real_Start + All_tasks[t].t_c[All_tasks[t].Real_Allocate] + All_tasks[t].t_s[All_tasks[t].Real_Allocate]
        Idle_time[M_r] = All_tasks[t].Real_Start + All_tasks[t].t_c[M_r]
    
    Temp = [[[0 for k in range (Jobs[i].D)] for j in range (Jobs[i].I)] for i in range (Num_of_Jobs)]
    result = 0
    for i in range (Num_of_Jobs):
        for j in range (Jobs[i].I):
            for k in range (Jobs[i].D):
                Temp[i][j][k] = Jobs[i].Tasks[j][k].Real_Complete
        DREAM_result[i] = max(max(Temp[i]))
        result += DREAM_result[i] * Jobs[i].weight
    
    return result
