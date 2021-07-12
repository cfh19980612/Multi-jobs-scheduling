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
    f = open('/Users/chenfahao/Desktop/Simulation/Test/result_Machines.txt','a')
    Num_of_Jobs = 50
    Num_of_Machines = 10
    # strs = 'random_ratio\n'
    strs = 'Job = 50\n'
    f.write(strs)

    # whether algorithms
    Is_FIFO = True
    Is_ALLOX = True
    Is_MM = True
    Is_Optimus = True
    Is_LP = True
    Is_DREAM = True

    t = 0
    while Num_of_Machines < 55:
        # generate jobs
        release_time = np.random.binomial(100, 0.5, size = Num_of_Jobs)
        # release_time = [0 for i in range (Num_of_Jobs)]

        Jobs = []
        # for i in range (Num_of_Jobs):
        #     Jobs.append(job(i,release_time[i],Num_of_Machines))

        for i in range (Num_of_Jobs): 
            if i < 1*Num_of_Jobs/3: # CV  
                Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'CV'))
            elif i >= 1*Num_of_Jobs/3 and i < 2*Num_of_Jobs/3: # NLP
                Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'NLP'))
            elif i >= 2*Num_of_Jobs/3:
                Jobs.append(Real_job(i,release_time[i],Num_of_Machines,'Rec'))
            # Jobs[i].Print_job()
        # FIFO
        if Is_FIFO: 
            FIFO_result_job, FIFO_result = FIFO_solver(Jobs, Num_of_Machines)
            f_FIFO = open('/Users/chenfahao/Desktop/Simulation/Test/cdf_FIFO.txt','w')
            print('FIFO Complete!')

        # Max_Min
        if Is_MM: 
            MM_result_job, MM_result = maxmin(Jobs, Num_of_Jobs, Num_of_Machines)
            f_MM = open('/Users/chenfahao/Desktop/Simulation/Test/cdf_MM.txt','w')
            print('Max-Min Complete!')

        # Optimus
        if Is_Optimus: 
            Opt_result = Optimus_Solver(Jobs, Num_of_Jobs, Num_of_Machines)
            print('Optimus Complete!')

        # Allox
        if Is_ALLOX: 
            Allox_result_job, Allox_result = Allox_Solver(Jobs,Num_of_Jobs, Num_of_Machines)
            f_Allox = open('/Users/chenfahao/Desktop/Simulation/Test/cdf_Allox.txt','w')
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
            f_LP = open('/Users/chenfahao/Desktop/Simulation/Test/cdf_DREAM.txt','w')
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
            DREAM_result_job, DREAM_result = DREAM(Jobs, Num_of_Machines, Num_of_Jobs, x_lp)
            f_Dream = open('/Users/chenfahao/Desktop/Simulation/Test/cdf_Optimus.txt','w')
            print('DREAM Complete!')

        # print result
        if Is_LP:
            if LP_result <= DREAM_result:
        # if True:
                print('Number of Machines: ',Num_of_Machines)
                # print('Number of Machines: ',Num_of_Machines)
                if Is_LP: print('LP-bound: ', LP_result)
                if Is_FIFO: print('FIFO-schedule: ', FIFO_result)
                if Is_MM: print('MM-schedule: ', MM_result)
                if Is_Optimus: print('Optimus-schedule: ', Opt_result)
                if Is_ALLOX: print('Allox-schedule: ', Allox_result)
                if Is_DREAM:print('DREAM: ', DREAM_result)

                # record the result
                start = 'Machines: ' + str(Num_of_Machines) + '  '
                # start = 'Machines: ' + str(Num_of_Machines) + '  '
                f.write(start)

                if Is_LP: 
                    LP_txt = str(LP_result) + '  '
                    f.write(LP_txt)
                    # JCT
                    LP_txt1 = str(LP_result_job) + '  \n'
                    LP_txt1 = LP_txt1.replace('[', '')
                    LP_txt1 = LP_txt1.replace(']', '')
                    LP_txt1 = LP_txt1.replace(',', '')
                    f_LP.write(LP_txt1)
                    f_LP.close()

                if Is_FIFO: 
                    FIFO_txt = str(FIFO_result) + '  '
                    f.write(FIFO_txt)

                    FIFO_txt1 = str(FIFO_result_job) + '  \n'
                    FIFO_txt1 = FIFO_txt1.replace('[', '')
                    FIFO_txt1 = FIFO_txt1.replace(']', '')
                    FIFO_txt1 = FIFO_txt1.replace(',', '')
                    f_FIFO.write(FIFO_txt1)
                    f_FIFO.close()

                if Is_MM: 
                    MM_txt = str(MM_result) + '  '
                    f.write(MM_txt)

                    MM_txt1 = str(MM_result_job) + '  \n'
                    MM_txt1 = MM_txt1.replace('[', '')
                    MM_txt1 = MM_txt1.replace(']', '')
                    MM_txt1 = MM_txt1.replace(',', '')
                    f_MM.write(MM_txt1)
                    f_MM.close()

                if Is_Optimus: 
                    Opt_txt = str(Opt_result) + '  '
                    f.write(Opt_txt)

                if Is_ALLOX: 
                    Allox_txt = str(Allox_result) + '  '
                    f.write(Allox_txt)

                    Allox_txt1 = str(Allox_result_job) + '  \n'
                    Allox_txt1 = Allox_txt1.replace('[', '')
                    Allox_txt1 = Allox_txt1.replace(']', '')
                    Allox_txt1 = Allox_txt1.replace(',', '')
                    f_Allox.write(Allox_txt1)
                    f_Allox.close()
                if Is_DREAM: 
                    DREAM_txt = str(DREAM_result) + '\n'
                    f.write(DREAM_txt)

                    DREAM_txt1 = str(DREAM_result_job) + '\n'
                    DREAM_txt1 = DREAM_txt1.replace('[', '')
                    DREAM_txt1 = DREAM_txt1.replace(']', '')
                    DREAM_txt1 = DREAM_txt1.replace(',', '')
                    f_Dream.write(DREAM_txt1)
                    f_Dream.close()

                Num_of_Machines += 5

                t += 1
            print()
    f.close()
if __name__ == "__main__":
    run()