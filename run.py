import numpy as np
import itertools
from FIFO import *
from Schedule import *
from Job_Environment import *
from LP import *
from DREAM import *
from GA import *


def run():
    
    f = open('result.txt','a')
    Num_of_Jobs = 30
    Num_of_Machines = 10

    for i in range (20):
        # generate jobs
        release_time = np.random.binomial(5, 0.5, size = Num_of_Jobs)
        # release_time = [0 for i in range (Num_of_Jobs)]
        Jobs = []
        for i in range (Num_of_Jobs):
            Jobs.append(job(i,release_time[i],Num_of_Machines))
            # Jobs[i].Print_job()
        # FIFO
        FIFO_result = FIFO_solver(Jobs, Num_of_Machines)

        # LP
        # length = 0 # the size of all tasks
        # for i in range (Num_of_Jobs):
        #     length += Jobs[i].D * Jobs[i].I
        # Random_allocation = np.random.randint(0,Num_of_Machines,length)
        # DLJS_lp = DLJS_LP(Jobs, Num_of_Jobs, Num_of_Machines)
        # x_lp, LP_result = DLJS_lp.LP_Solver(Random_allocation)
        # LP-GA

        x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)

        # for i in range (Num_of_Jobs):
        #     for j in range (Jobs[i].I):
        #         for k in range (Jobs[i].D):
        #             print(Jobs[i].Tasks[j][k].P)
                    # print(Jobs[i].Tasks[j][k].Real_Allocate)
        # DREAM 
        DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)

        # print result
        print('LP-bound: ', LP_result)
        print('FIFO-schedule: ', FIFO_result)
        print('DREAM: ', DREAM_result)

        if LP_result < DREAM_result:
            Num_of_Jobs += 10
            # record the result
            start = 'JOBS: ' + str(Num_of_Jobs) + '  '
            LP_txt = 'LP: ' + str(LP_result) + '  '
            FIFO_txt = 'FIFO: ' + str(FIFO_result) + '  '
            DREAM_txt = 'DREAM: ' + str(DREAM_result) + '\n'

            f.write(start)
            f.write(LP_txt)
            f.write(FIFO_txt)
            f.write(DREAM_txt)

    f.close()
if __name__ == "__main__":
    run()