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
from update_LP import *

def run():
    Num_of_Jobs = 30
    Num_of_Machines = 5

    # whether algorithms
    Is_FIFO = False
    Is_ALLOX = False
    Is_MM = False
    Is_Optimus = False
    Is_LP = True
    Is_DREAM = True
    t = 0


    # generate jobs
    # release_time = np.random.binomial(100, 0.5, size = Num_of_Jobs)
    # release_time = [random.randint(0,1000) for i in range (Num_of_Jobs)]
    release_time = [0 for i in range (Num_of_Jobs)]

    Jobs = []

    for i in range (Num_of_Jobs):
        Jobs.append(job(i,release_time[i],Num_of_Machines))

    # 3:5:2
    # for i in range (Num_of_Jobs): 
    #     if i < 3*Num_of_Jobs/10: # CV  
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'CV'))
    #     elif i >= 3*Num_of_Jobs/10 and i < 8*Num_of_Jobs/10: # NLP
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'NLP'))
    #     elif i >= 8*Num_of_Jobs/10:
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'Rec'))

    # 1:1:1
    # for i in range (Num_of_Jobs): 
    #     if i < 1*Num_of_Jobs/3: # CV  
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'CV'))
    #     elif i >= 1*Num_of_Jobs/3 and i < 2*Num_of_Jobs/3: # NLP
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'NLP'))
    #     elif i >= 2*Num_of_Jobs/3:
    #         Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'Rec'))

        # Jobs[i].Print_job()
    # FIFO
    if Is_FIFO: 
        FIFO_result_job, FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
        f_FIFO = open('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_FIFO.txt','w')
        print('FIFO Complete!')

    # Max_Min
    if Is_MM: 
        MM_result_job, MM_result = maxmin(Jobs, Num_of_Jobs, Num_of_Machines)
        f_MM = open('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_MM.txt','w')
        print('Max-Min Complete!')

    # Optimus
    if Is_Optimus: 
        Opt_result = Optimus_Solver(Jobs, Num_of_Jobs, Num_of_Machines)
        # f_Opt = open('/Users/chenfahao/Desktop/Simulation/Test/result_testbed.txt','a')
        print('Optimus Complete!')

    # Allox
    if Is_ALLOX: 
        Allox_result_job, Allox_result = Allox_Solver(Jobs,Num_of_Jobs, Num_of_Machines)
        f_Allox = open('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Allox.txt','w')
        print('Allox Complete!')

    # LP-GA
        # x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)

    # DLJS-LP
    if Is_LP:
        # LP = LP_Solver(Jobs, Num_of_Jobs, Num_of_Machines)
        # x_lp, LP_result, LP_result_job = LP.Solver()
        length = 0 # the size of all tasks
        for i in range (Num_of_Jobs):
            length += Jobs[i].D * Jobs[i].I
        Random_allocation = np.random.randint(0,Num_of_Machines,length)
        m_lp, x_lp, LP_result, LP_result_job = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, Random_allocation)
        f_LP = open('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_DREAM.txt','w')
        print('LP Complete!')

    # DREAM 
    if Is_DREAM: 
        DREAM_result_job, DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)
        f_Dream = open('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Optimus.txt','w')
        #f_Opt = open('/Users/chenfahao/Desktop/Simulation/Test/result_testbed.txt','a')
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
    # start = 'Jobs: ' + str(Num_of_Jobs) + '  '
    # # start = 'Machines: ' + str(Num_of_Machines) + '  '
    # f.write(start)

    if Is_LP: 
        # LP_txt = str(LP_result) + str(LP_result_job) + '  \n'
        LP_txt = str(LP_result_job) + '  \n'
        LP_txt = LP_txt.replace('[', '')
        LP_txt = LP_txt.replace(']', '')
        LP_txt = LP_txt.replace(',', '')
        f_LP.write(LP_txt)
        f_LP.close()

    if Is_FIFO: 
        # FIFO_txt = str(FIFO_result) + str(FIFO_result_job) + '  \n'
        FIFO_txt = str(FIFO_result_job) + '  \n'
        FIFO_txt = FIFO_txt.replace('[', '')
        FIFO_txt = FIFO_txt.replace(']', '')
        FIFO_txt = FIFO_txt.replace(',', '')
        f_FIFO.write(FIFO_txt)
        f_FIFO.close()

    if Is_MM: 
        # MM_txt = str(MM_result) + str(MM_result_job) + '  \n'
        MM_txt = str(MM_result_job) + '  \n'
        MM_txt = MM_txt.replace('[', '')
        MM_txt = MM_txt.replace(']', '')
        MM_txt = MM_txt.replace(',', '')
        f_MM.write(MM_txt)
        f_MM.close()

    if Is_Optimus: 
        Opt_txt = str(Opt_result) + '  \n'
        # f.write(Opt_txt)

    if Is_ALLOX: 
        # Allox_txt = str(Allox_result) + str(Allox_result_job) + '  \n'
        Allox_txt = str(Allox_result_job) + '  \n'
        Allox_txt = Allox_txt.replace('[', '')
        Allox_txt = Allox_txt.replace(']', '')
        Allox_txt = Allox_txt.replace(',', '')
        f_Allox.write(Allox_txt)
        f_Allox.close()

    if Is_DREAM: 
        # DREAM_txt = str(DREAM_result) + str(DREAM_result_job) + '\n'
        DREAM_txt = str(DREAM_result_job) + '\n'
        DREAM_txt = DREAM_txt.replace('[', '')
        DREAM_txt = DREAM_txt.replace(']', '')
        DREAM_txt = DREAM_txt.replace(',', '')
        f_Dream.write(DREAM_txt)
        f_Dream.close()
if __name__ == "__main__":
    run()