import random
from LP_M import *
from LP_X import *

def DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, Allocation):
    eta = 100
    optimal_m = []
    optimal_x = []
    optimal_j = []
    optimal = 0
    # generate two linear programming LP_M and LP_X
    LP_m = LPM(Jobs, Num_of_Jobs, Num_of_Machines)
    LP_x = LPX(Jobs, Num_of_Jobs, Num_of_Machines)

    # randomly generate a allocation
    # length = 0
    # for i in range (Num_of_Jobs):
    #     length += Jobs[i].D * Jobs[i].I
    # optimal_m = np.random.randint(0,Num_of_Machines,length)
    optimal_m = Allocation
    idx = 0
    while (eta > 0.009):
        # step 1
        temp_x, result_m = LP_m.LP_M_Solver(optimal_m)
        optimal_x = temp_x

        # step 2
        temp_m, result_x, optimal_j = LP_x.LP_X_Solver(optimal_x)
        optimal_m = temp_m

        #step 3
        eta = abs(result_m/result_x - 1)

        optimal = result_m
        print('round: ', idx+1, ' eta: ', eta, ' LP-bound: ', optimal)
        idx += 1
    return optimal_m, optimal_x, optimal, optimal_j
