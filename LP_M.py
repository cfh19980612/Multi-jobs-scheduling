import gurobipy as gp
import numpy as np
import math
from gurobipy import GRB
from Job_Environment import *
from Task_Environment import *

class LPM:
    def __init__(self,Jobs, Num_of_Jobs, Num_of_Machines):
        super().__init__()
        self.Jobs = Jobs
        self.Num_of_Jobs = Num_of_Jobs
        self.Num_of_Machines = Num_of_Machines

    def LP_M_Solver(self, solution):    # solve the LP problem with a given allocation mapping m

        # initial
        for i in range (self.Num_of_Jobs):
            for j in range (self.Jobs[i].I):
                for k in range (self.Jobs[i].D):
                    for l in range (self.Num_of_Machines):
                        self.Jobs[i].Tasks[j][k].P[l] = 0

        Result = [[[0 for k in range (self.Jobs[i].D)] for j in range (self.Jobs[i].I)] for i in range (self.Num_of_Jobs)]
        Result_Job = [0 for i in range (self.Num_of_Jobs)]
        # generate a random allocation (API)
        idx = 0
        for i in range (self.Num_of_Jobs):
            for j in range (self.Jobs[i].I):
                for k in range (self.Jobs[i].D):
                    self.Jobs[i].Tasks[j][k].Allocate = solution[idx]
                    self.Jobs[i].Tasks[j][k].P[self.Jobs[i].Tasks[j][k].Allocate] += 1
                    idx += 1
        try:
            # Create a new model
            m = gp.Model("LP-M")
            m.setParam('OutputFlag', 0)

            # Create variables
            x = [None for i in range (self.Num_of_Jobs)]  # start time
            C = m.addVars(self.Num_of_Jobs, lb = 0, vtype = GRB.CONTINUOUS, name = 'c')  # completion time
            for i in range (self.Num_of_Jobs):
                x[i] = m.addVars(self.Jobs[i].I, self.Jobs[i].D, lb = 0, vtype = GRB.CONTINUOUS,name = 'x')

            # constraint 1: x_i >= r_n 
            for i in range (self.Num_of_Jobs):
                for j in range (self.Jobs[i].I):
                    for k in range (self.Jobs[i].D):
                        m.addConstr(x[i][j,k] >= self.Jobs[i].r)
            # for i in range (len(Tasks)):
            #     m.addConstr(x[i] >= Jobs[x[i].job_id].r)

            # constraint 2: x_j >= x_i + Tc_i + Ts_i, i in I_e, j in I_(e+1)
            for i in range (self.Num_of_Jobs):
                for j in range (self.Jobs[i].I - 1):
                    for k in range (self.Jobs[i].D):
                        for l in range (self.Jobs[i].D):
                            m.addConstr(x[i][j,k] + self.Jobs[i].Tasks[j][k].t_c[self.Jobs[i].Tasks[j][k].Allocate] + self.Jobs[i].Tasks[j][k].t_s[self.Jobs[i].Tasks[j][k].Allocate] <= x[i][j+1,l])

            # constraint 3: C_n >= x_i + Tc_i + Ts_i, forall i
            for i in range (self.Num_of_Jobs):
                for k in range (self.Jobs[i].D):
                    m.addConstr(C[i] >= x[i][self.Jobs[i].I-1,k] + self.Jobs[i].Tasks[self.Jobs[i].I-1][k].t_c[self.Jobs[i].Tasks[self.Jobs[i].I-1][k].Allocate] + \
                        self.Jobs[i].Tasks[self.Jobs[i].I-1][k].t_s[self.Jobs[i].Tasks[self.Jobs[i].I-1][k].Allocate])
            
            # constraint 4: 
            # for m in range (Num_of_Machines):
            #     m.addConstr(quicksum(quicksum(quicksum(quicksum(Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]\
            #         *(x[i][j,k] + Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate])*Jobs[i].Tasks[j][k].P[l] for l in range (Num_of_Machines)) \
            #             for k in Jobs[i].D) for j in Jobs[i].I) for i in range(Num_of_Jobs)) <= pow(quicksum(quicksum(quicksum(\
            #                 Jobs[i].Tasks[j][k].t_c[Jobs[i].Tasks[j][k].Allocate]*Jobs[i].Tasks[j][k].P[l] for l in range (Num_of_Machines)) for k in range (Jobs[i].D) for j in range (Jobs[i].I))),2))

            for o in range (self.Num_of_Machines):
                m.addConstr(gp.quicksum(self.Jobs[i].Tasks[j][k].t_c[o]*(x[i][j,k] + self.Jobs[i].Tasks[j][k].t_c[o])*self.Jobs[i].Tasks[j][k].P[o] \
                    for i in range (self.Num_of_Jobs) for j in range (self.Jobs[i].I) for k in range (self.Jobs[i].D)) >= \
                        pow(gp.quicksum(self.Jobs[i].Tasks[j][k].t_c[o]*self.Jobs[i].Tasks[j][k].P[o] for i in range (self.Num_of_Jobs) \
                            for j in range (self.Jobs[i].I) for k in range (self.Jobs[i].D)),2)/2 + \
                            gp.quicksum(pow(self.Jobs[i].Tasks[j][k].t_c[o]*self.Jobs[i].Tasks[j][k].P[o],2) for i in range (self.Num_of_Jobs) \
                            for j in range (self.Jobs[i].I) for k in range (self.Jobs[i].D))/2\
                            )

            # object
            m.setObjective(gp.quicksum(C[i]*self.Jobs[i].weight for i in range (self.Num_of_Jobs)), GRB.MINIMIZE)

            # Optimize model
            m.optimize()
            # print('schedule:' ,m.x)
            # print('Obj: %g' % m.objVal)
            
            for i in range (self.Num_of_Jobs):
                Result_Job[i] = C[i].x
                for j in range (self.Jobs[i].I):
                    for k in range (self.Jobs[i].D):
                        Result[i][j][k] = x[i][j,k].x
        
            return Result, m.objVal

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))

        except AttributeError:
            print('Encountered an attribute error')



