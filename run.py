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
    f = open('/Users/chenfahao/Desktop/Simulation/Test/result_ratio.txt','a')
    Num_of_Jobs = 40
    Num_of_Machines = 40
    # strs = 'random_ratio\n'
    strs = 'Machine = 40, Job = 30\n'
    f.write(strs)

    # whether algorithms
    Is_FIFO = False
    Is_ALLOX = False
    Is_MM = False
    Is_Optimus = False
    Is_LP = True
    Is_DREAM = True

    t = 0
    while Num_of_Jobs < 72:
        # generate jobs
        release_time = np.random.binomial(5, 0.5, size = Num_of_Jobs)
        # release_time = [0 for i in range (Num_of_Jobs)]

        Jobs = []
        for i in range (Num_of_Jobs):
            Jobs.append(job(i,release_time[i],Num_of_Machines))
            # Jobs[i].Print_job()
        # FIFO
        if Is_FIFO: 
            FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
            print('FIFO Complete!')

        # Max_Min
        if Is_MM: 
            MM_result = maxmin(Jobs, Num_of_Jobs, Num_of_Machines)
            print('Max-Min Complete!')

        # Optimus
        if Is_Optimus: 
            Opt_result = Optimus_Solver(Jobs, Num_of_Jobs, Num_of_Machines)
            print('Optimus Complete!')

        # Allox
        if Is_ALLOX: 
            Allox_result = Allox_Solver(Jobs,Num_of_Jobs, Num_of_Machines)
            print('Allox Complete!')

        # LP-GA
            # x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)

        # DLJS-LP
        if Is_LP:
            length = 0 # the size of all tasks
            for i in range (Num_of_Jobs):
                length += Jobs[i].D * Jobs[i].I
            Random_allocation = np.random.randint(0,Num_of_Machines,length)
            m_lp, x_lp, LP_result = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, Random_allocation)
            print('LP Complete!')

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
        if Is_DREAM: 
            DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)
            print('DREAM Complete!')

        # print result
        if Is_LP:
            if LP_result <= DREAM_result:
        # if True:
                print('Number of Jobs: ',Num_of_Jobs)
                # print('Number of Machines: ',Num_of_Machines)
                if Is_LP: print('LP-bound: ', LP_result)
                if Is_FIFO: print('FIFO-schedule: ', FIFO_result)
                if Is_MM: print('MM-schedule: ', MM_result)
                if Is_Optimus: print('Optimus-schedule: ', Opt_result)
                if Is_ALLOX: print('Allox-schedule: ', Allox_result)
                if Is_DREAM:print('DREAM: ', DREAM_result/LP_result)

                # record the result
                start = 'Jobs: ' + str(Num_of_Jobs) + '  '
                # start = 'Machines: ' + str(Num_of_Machines) + '  '
                f.write(start)

                if Is_LP: 
                    LP_txt = str(LP_result) + '  '
                    f.write(LP_txt)

                if Is_FIFO: 
                    FIFO_txt = str(FIFO_result) + '  '
                    f.write(FIFO_txt)

                if Is_MM: 
                    MM_txt = str(MM_result) + '  '
                    f.write(MM_txt)

                if Is_Optimus: 
                    Opt_txt = str(Opt_result) + '  '
                    f.write(Opt_txt)

                if Is_ALLOX: 
                    Allox_txt = str(Allox_result) + '  '
                    f.write(Allox_txt)
                if Is_DREAM: 
                    DREAM_txt = str(DREAM_result/LP_result) + '\n'
                    f.write(DREAM_txt)

                # Num_of_Jobs += 2

                t += 1
            print()
    f.close()
if __name__ == "__main__":
    run()