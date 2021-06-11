import numpy as np
import itertools
from FIFO import *
from Schedule import *
from Job_Environment import *
from LP import *
from DREAM import *
from GA import *
Num_of_Jobs = 10
Num_of_Machines = 10

def run():
    # generate jobs
    release_time = np.random.binomial(10, 0.5, size = Num_of_Jobs)
    # release_time = [0 for i in range (Num_of_Jobs)]
    Jobs = []
    for i in range (Num_of_Jobs):
        Jobs.append(job(i,release_time[i],Num_of_Machines))
        # Jobs[i].Print_job()
    # FIFO
    FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
    # LP
    #DLJS_lp = DLJS_LP(Jobs, Num_of_Jobs, Num_of_Machines)
    x_lp, LP_result = ga(Num_of_Jobs, Num_of_Machines, Jobs)
    # print(x_lp)
    # DREAM 
    DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)

    # print result
    print('LP-bound: ', LP_result)
    print('FIFO-schedule: ', FIFO_result)
    print('DREAM: ', DREAM_result)

if __name__ == "__main__":
    run()