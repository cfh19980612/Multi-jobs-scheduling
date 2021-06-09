import numpy as np
import itertools
from FIFO import *
from Schedule import *
from Job_Environment import *
from LP import *

Num_of_Jobs = 10
Num_of_Machines = 100

def run():
    # generate jobs
    release_time = np.random.binomial(10, 0.5, size = Num_of_Jobs)
    Jobs = []
    for i in range (Num_of_Jobs):
        Jobs.append(job(i,release_time[i],Num_of_Machines))
    
    # FIFO
    # FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
    # LP
    LP_result = LP_Solver(Jobs, Num_of_Jobs, Num_of_Machines)

    # print('FIFO-schedule: ', FIFO_result)
    print('LP-bound: ', LP-result)

if __name__ == "__main__":
    run()