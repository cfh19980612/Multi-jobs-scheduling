import gurobipy as gp
import numpy as np
import math
from gurobipy import GRB
from Job_Environment import *
from Task_Environment import *

def Optimus_Solver(Jobs, Num_of_Jobs, Num_of_Machines):
    Selection_scale = 15 # 每一轮选择任务的个数
    Time = 0 # 总完成时间
    base_time = 0 # 下一轮开始的基础时间
    Preemption = sorted(range(len(Jobs)), key=lambda x: Jobs[x].r, reverse=False) # 按照到来时间排序
    ID_temp = Preemption 

    if Selection_scale >= len(Jobs):
        Select = Preemption
    else: Select = Preemption[:Selection_scale:1]
    while(len(Select) != 0):
        # 按照到来顺序选择前Selection_scale个任务
        Job_select = []
        for i in range (len(Select)):
            Job_select.append(Jobs[Select[i]])

        # 分配加放置
        Allocation = Resource_Allocation(Job_select, len(Job_select), Num_of_Machines)
        Placement = Task_Placement(Job_select, len(Job_select), Num_of_Machines, Allocation)
        # print(Allocation,Placement)

        # total rounds for each jobs
        R = [0 for i in range (len(Job_select))]
        for i in range (len(Job_select)):
            if Allocation[i] != 0:
                R[i] = math.ceil(Job_select[i].D/Allocation[i])
        Processing_time = [[0 for i in range (Num_of_Machines)] for j in range (len(Job_select))]
        max_time = 0
        cost_time = [0 for i in range (len(Job_select))]
        for i in range (len(Job_select)):
            if Allocation[i] != 0:
                Processing_time[i] = [Job_select[i].t_c[j]+Job_select[i].t_c[j] for j in range(min(len(Job_select[i].t_c),len(Job_select[i].t_s)))]
                cost_time[i] = Job_select[i].I*R[i]*max([Processing_time[i][j]*Placement[i][j] for j in range (Num_of_Machines)]) #w_i * I * R * T
                if max_time < cost_time[i]: max_time = cost_time[i]
        base_time += max_time
        for i in range (len(Job_select)):
            Time += Job_select[i].weight*(base_time + cost_time[i])

        # Next round selection
        ID_rest = []
        # 上一轮未调度的任务：
        for i in range (len(Select)):
            if Allocation[i] == 0:
                ID_rest.append(Select[i])
        # 上一轮未被选择的任务：
        for i in range (len(ID_temp)):
            if ID_temp[i] not in Select:
                ID_rest.append(ID_temp[i])
        # 剩余未调度任务集合
        ID_temp = ID_rest
        # 选择前Selection_scale个任务
        if Selection_scale >= len(ID_temp):
            Select = ID_temp
        else: Select = ID_temp[:Selection_scale:1]
    return Time

def Resource_Allocation(Jobs, Num_of_Jobs, Num_of_Machines):
    Result = [0 for i in range (Num_of_Jobs)]
    try:
        # Create a new model
        m = gp.Model("Allocation")
        # m.params.NonConvex = 2
        m.setParam('OutputFlag', 0)

        # Create variables
        x = m.addVars(Num_of_Jobs, lb = 0, ub = Num_of_Machines, vtype = GRB.INTEGER, name = 'x')  # number of allocated machines

        # Create constraints
        m.addConstr(gp.quicksum(x[i] for i in range (Num_of_Jobs)) <= Num_of_Machines)
        for i in range (Num_of_Jobs):
            m.addConstr(x[i] <= Jobs[i].D )

        # Total speed
        Time_spend = 0
        T_c = [0 for i in range (Num_of_Jobs)]
        T_s = [0 for i in range (Num_of_Jobs)]
        for i in range (Num_of_Jobs):
            T_c[i] = max(Jobs[i].t_c)
            T_s[i] = max(Jobs[i].t_s)
            # Time_spend += Jobs[i].I*(T_c[i] + T_s[i] + (Jobs[i].D*y[i] - 1)*max(T_c[i],T_s[i]))
            Time_spend +=Jobs[i].weight * x[i] * 1/(Jobs[i].I*Jobs[i].D*(T_c[i] + T_s[i]))

        # object
        m.setObjective(Time_spend, GRB.MAXIMIZE)

        # Optimize model
        m.optimize()
        # print('Obj: %g' % m.objVal)
        
        for i in range (Num_of_Jobs):
            Result[i] = x[i].x

        return Result

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

def Task_Placement(Jobs, Num_of_Jobs, Num_of_Machines, Allocation):
    Result = [[0 for i in range (Num_of_Machines)] for j in range (Num_of_Jobs)]
    try:
        # Create a new model
        m = gp.Model("Placement")
        # m.params.NonConvex = 2
        m.setParam('OutputFlag', 0)

        # Create variables
        y = [None for i in range (Num_of_Jobs)]
        for i in range (Num_of_Jobs):
            y[i] = m.addVars(Num_of_Machines, lb = 0, ub = 1, vtype = GRB.BINARY, name = 'y')  # number of allocated machines

        # Create constraints
        # m.addConstr(gp.quicksum(x[i] for i in range (Num_of_Jobs)) <= Num_of_Machines)
        for i in range (Num_of_Jobs):
            m.addConstr(gp.quicksum(y[i][j] for j in range (Num_of_Machines)) == Allocation[i])

        # Object
        Time_spend = 0
        for i in range (Num_of_Jobs):
            # Time_spend += Jobs[i].I*(T_c[i] + T_s[i] + (Jobs[i].D*y[i] - 1)*max(T_c[i],T_s[i]))
            Time_spend += gp.quicksum(Jobs[i].t_c[j]*y[i][j] + Jobs[i].t_s[j]*y[i][j] for j in range (Num_of_Machines))

        # object
        m.setObjective(Time_spend, GRB.MINIMIZE)

        # Optimize model
        m.optimize()
        # print('Obj: %g' % m.objVal)
        
        for i in range (Num_of_Jobs):
            for j in range (Num_of_Machines):
                Result[i][j] = y[i][j].x

        return Result

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')