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

def run():
    f = open('result2.txt','a')
    Num_of_Jobs = 5
    Num_of_Machines = 10
    strs = 'Random_size\n'
    f.write(strs)

    while Num_of_Jobs < 55:
        # generate jobs
        # release_time = np.random.binomial(2, 0.5, size = Num_of_Jobs)
        release_time = [0 for i in range (Num_of_Jobs)]

        Jobs = []
        for i in range (Num_of_Jobs):
            Jobs.append(job(i,release_time[i],Num_of_Machines))
            # Jobs[i].Print_job()
        # FIFO
        FIFO_result = FIFO_solver(Jobs, Num_of_Machines)

        # Allox
        Allox_result = Allox_Solver(Jobs,Num_of_Jobs, Num_of_Machines)
        # LP
        # length = 0 # the size of all tasks
        # for i in range (Num_of_Jobs):
        #     length += Jobs[i].D * Jobs[i].I
        # Random_allocation = np.random.randint(0,Num_of_Machines,length)
        # DLJS_lp = DLJS_LP(Jobs, Num_of_Jobs, Num_of_Machines)
        # x_lp, LP_result = DLJS_lp.LP_Solver(Random_allocation)

        # LP-GA
        x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)

        # DLJS-LP
        # m_lp, x_lp, LP_result = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs)

        # LP_M
        # length = 0 # the size of all tasks
        # for i in range (Num_of_Jobs):
        #     length += Jobs[i].D * Jobs[i].I
        # m = np.random.randint(0,Num_of_Machines,length)
        # LP_m = LPM(Jobs, Num_of_Jobs, Num_of_Machines)
        # x_lp, LP_result = LP_m.LP_M_Solver(m)
        # print(x_lp, LP_result)

        # LP_X
        # x_lp = [[[0.0, 0.0], [0.2, 0.2]], [[0.0666666666666667, 0.06666666666666671], [0.2666666666666667, 0.2666666666666667]]]
        # LP_x = LPX(Jobs, Num_of_Jobs, Num_of_Machines)
        # m, LP_result = LP_x.LP_X_Solver(x_lp)
        # print (m, LP_result)

        # DREAM 
        DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)

        # print result

        if LP_result <= DREAM_result:
            print('Number of Jobs: ',Num_of_Jobs)
            print('LP-bound: ', LP_result)
            print('FIFO-schedule: ', FIFO_result)
            print('Allox-schedule: ', Allox_result)
            print('DREAM: ', DREAM_result)
            # record the result
            start = 'JOBS: ' + str(Num_of_Jobs) + '  '
            # LP_txt = 'LP: ' + str(LP_result) + '  '
            FIFO_txt = 'FIFO: ' + str(FIFO_result/LP_result) + '  '
            Allox_txt = 'Allox: '+ str(Allox_result/LP_result) + '  '
            DREAM_txt = 'DREAM: ' + str(DREAM_result/LP_result) + '\n'
            f.write(start)
            # f.write(LP_txt)
            f.write(FIFO_txt)
            f.write(Allox_txt)
            f.write(DREAM_txt)
            Num_of_Jobs += 5
        print()
    f.close()
if __name__ == "__main__":
    run()