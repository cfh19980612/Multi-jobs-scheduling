from __future__ import division
import numpy as np
import itertools
from FIFO import *
from Schedule import *
from Job_Environment import *
from DREAM import *
from GA import *
from DLJS_LP import *
from Allox import *
from Max_Min import *
from Optimus import *
from Real_trace import *

def run():
    f = open('/Users/chenfahao/Desktop/Simulation/Test/result_testbed.txt','a')
    Num_of_Jobs = 20
    Num_of_Machines = 10
    # strs = 'random_ratio\n'
    strs = 'Machine = 40, Job = 30\n'
    f.write(strs)

    # whether algorithms
    Is_FIFO = True
    Is_ALLOX = True
    Is_MM = True
    Is_Optimus = True
    Is_LP = True
    Is_DREAM = True
    t = 0

    # generate jobs
    release_time = np.random.binomial(5, 0.5, size = Num_of_Jobs)
    # release_time = [0 for i in range (Num_of_Jobs)]

    Jobs = []  
    for i in range (Num_of_Jobs): 
        if i < Num_of_Jobs/3: # CV  
            Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'CV'))
        elif i >= Num_of_Jobs/3 and i < 2*Num_of_Jobs/3: # NLP
            Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'NLP'))
        elif i >= 2*Num_of_Jobs/3:
            Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'Rec'))
        # Jobs[i].Print_job()
    # FIFO
    if Is_FIFO: 
        FIFO_result_job, FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
        print('FIFO Complete!')

    # Max_Min
    if Is_MM: 
        MM_result_job, MM_result = maxmin(Jobs, Num_of_Jobs, Num_of_Machines)
        print('Max-Min Complete!')

    # Optimus
    if Is_Optimus: 
        Opt_result = Optimus_Solver(Jobs, Num_of_Jobs, Num_of_Machines)
        print('Optimus Complete!')

    # Allox
    if Is_ALLOX: 
        Allox_result_job, Allox_result = Allox_Solver(Jobs,Num_of_Jobs, Num_of_Machines)
        print('Allox Complete!')

    # LP-GA
        # x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)

    # DLJS-LP
    if Is_LP:
        length = 0 # the size of all tasks
        for i in range (Num_of_Jobs):
            length += Jobs[i].D * Jobs[i].I
        Random_allocation = np.random.randint(0,Num_of_Machines,length)
        m_lp, x_lp, LP_result, LP_result_job = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, Random_allocation)
        print('LP Complete!')

    # DREAM 
    if Is_DREAM: 
        DREAM_result_job, DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)
        print('DREAM Complete!')

    # print result
    # if True:
    print('Number of Jobs: ',Num_of_Jobs)
    # print('Number of Machines: ',Num_of_Machines)
    if Is_LP: print('LP-bound: ', LP_result)
    if Is_FIFO: print('FIFO-schedule: ', FIFO_result)
    if Is_MM: print('MM-schedule: ', MM_result)
    if Is_Optimus: print('Optimus-schedule: ', Opt_result)
    if Is_ALLOX: print('Allox-schedule: ', Allox_result)
    if Is_DREAM:print('DREAM: ', DREAM_result)

    # record the result
    start = 'Jobs: ' + str(Num_of_Jobs) + '  '
    # start = 'Machines: ' + str(Num_of_Machines) + '  '
    f.write(start)

    if Is_LP: 
        LP_txt = str(LP_result) + str(LP_result_job) + '  '
        f.write(LP_txt)

    if Is_FIFO: 
        FIFO_txt = str(FIFO_result) + str(FIFO_result_job) + '  '
        f.write(FIFO_txt)

    if Is_MM: 
        MM_txt = str(MM_result) + str(MM_result_job) + '  '
        f.write(MM_txt)

    if Is_Optimus: 
        Opt_txt = str(Opt_result) + '  '
        f.write(Opt_txt)

    if Is_ALLOX: 
        Allox_txt = str(Allox_result) + str(Allox_result_job) + '  '
        f.write(Allox_txt)
    if Is_DREAM: 
        DREAM_txt = str(DREAM_result) + str(DREAM_result_job) + '\n'
        f.write(DREAM_txt)
        print()
    f.close()
if __name__ == "__main__":
    run()