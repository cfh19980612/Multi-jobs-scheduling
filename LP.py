import gurobipy as gp
import numpy as np
import math
from gurobipy import GRB
from Job_Environment import *
from Task_Environment import *

def LP_Solver(Jobs, Num_of_Jobs, Num_of_Machines):
    Num_of_jobs = range(Num_of_Jobs)
    Num_of_machines = range(Num_of_Machines)

    # generate a random allocation
    for i in range (Num_of_Jobs):
        for j in range (Jobs[i].I):
            for k in range (Jobs[i].D):
                Jobs[i].Tasks[j][k].Allocate = np.random.randint(0,Num_of_Machines,1)[0]
                Jobs[i].Tasks[j][k].P[Jobs[i].Tasks[j][k].Allocate] = 1
    try:
        # Create a new model
        m = gp.Model("LP")

        # Create variables
        x = [None for i in range (len(Jobs))]  # start time
        C = m.addVars(len(Jobs), lb = 0, vtype = GRB.CONTINUOUS, name = 'x')  # completion time
        for i in range (len(Jobs)):
            x[i] = m.addVars(Jobs[i].I, Jobs[i].D, lb = 0, vtype = GRB.CONTINUOUS,name = 'x')

        # constraint 1: x_i >= r_n 
        for i in range (Num_of_Jobs):
            for j in range (Jobs[i].I):
                for k in range (Jobs[i].D):
                    m.addConstr(x[i][j,k] >= Jobs[i].r)
        # for i in range (len(Tasks)):
        #     m.addConstr(x[i] >= Jobs[x[i].job_id].r)

        # constraint 2: x_j >= x_i + Tc_i + Ts_i, i in I_e, j in I_(e+1)
        for i in range (Num_of_Jobs):
            for j in range (Jobs[i].I - 1):
                for k in range (Jobs[i].D):
                    for l in range (Jobs[i].D):
                        m.addConstr(x[i][j,k] + Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate] + Jobs[i].Tasks[j][k].t_s[Jobs[i].Tasks[j][k].Allocate] <= x[i][j+1,l])

        # constraint 3: C_n >= x_i + Tc_i + Ts_i, forall i
        for i in range (Num_of_Jobs):
            for j in range (Jobs[i].I):
                for k in range (Jobs[i].D):
                    m.addConstr(C[i] >= x[i][j,k] + Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate] + Jobs[i].Tasks[j][k].t_s[Jobs[i].Tasks[j][k].Allocate])
        
        # constraint 4: 
        # for m in range (Num_of_Machines):
        #     m.addConstr(quicksum(quicksum(quicksum(quicksum(Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]\
        #         *(x[i][j,k] + Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate])*Jobs[i].Tasks[j][k].P[l] for l in range (Num_of_Machines)) \
        #             for k in Jobs[i].D) for j in Jobs[i].I) for i in range(Num_of_Jobs)) <= pow(quicksum(quicksum(quicksum(\
        #                 Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]*Jobs[i].Tasks[j][k].P[l] for l in range (Num_of_Machines)) for k in range (Jobs[i].D) for j in range (Jobs[i].I))),2))
        for o in range (Num_of_Machines):
            m.addConstr(gp.quicksum(Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]*(x[i][j,k] + Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate])*Jobs[i].Tasks[j][k].P[l] \
                for i in range (Num_of_Jobs) for j in range (Jobs[i].I) for k in range (Jobs[i].D) for l in range (Num_of_Machines)) <= \
                    pow(gp.quicksum(Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]*Jobs[i].Tasks[j][k].P[l] for i in range (Num_of_Jobs) \
                        for j in range (Jobs[i].I) for k in range (Jobs[i].D) for l in range (Num_of_Machines)),2)/2 + \
                        gp.quicksum(pow(Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]*Jobs[i].Tasks[j][k].P[l],2) for i in range (Num_of_Jobs) \
                        for j in range (Jobs[i].I) for k in range (Jobs[i].D) for l in range (Num_of_Machines))/2\
                        )

        # object
        m.setObjective(gp.quicksum(C[i]*Jobs[i].weight for i in range (Num_of_Machines)), GRB.MINIMIZE)

        # Optimize model
        m.optimize()
        # print('schedule:' ,m.x)
        # print('Obj: %g' % m.objVal)
        return m.objVal

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


