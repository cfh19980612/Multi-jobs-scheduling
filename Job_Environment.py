import random
import numpy as np
from Task_Environment import *

class job:
    def __init__(self,job_id,time,machines):
        super().__init__()
        # self.E = random.randint(50,200)       # number of epoches
        # self.D = random.randint(5,100)        # number of chunks, i.e., number of tasks in each iteration
        # self.B = random.randint(10,100)       # number of mini-batches in each chunk

        #simple
        self.E = random.randint(1,2)
        self.D = random.randint(5,machines)
        self.B = random.randint(1,2)

        ###########################################################
        # fixed job scale
        # self.E = 1
        # self.D = 2
        # self.B = 2
        ###########################################################

        self.I = self.E*self.B                # number of iterations
        self.r = time                         # release time

        self.Tasks = []
        self.t_c = np.random.randint(1, 6, machines)/100
        self.t_s = np.random.randint(6, 10, machines)/100
        # self.t_c = [0.03 for i in range (machines)]
        # self.t_s = [0.06 for i in range (machines)]
        self.weight = np.random.rand(1)[0]

        ###########################################################
        # # fixed job parameter
        # self.t_c = [0.1 for i in range (machines)]
        # self.t_s = [0.1 for i in range (machines)]
        # self.weight = 1
        ###########################################################

        # for LP
        for i in range (self.I):
            temp = []
            for j in range (self.D):
                temp.append(task(job_id,i,machines,self.t_c,self.t_s))
            self.Tasks.append(temp)

    def Print_job(self):
        print('training time: ', self.t_c)
        print('synchronization time: ', self.t_s)
        print('release time: ',self.r)

