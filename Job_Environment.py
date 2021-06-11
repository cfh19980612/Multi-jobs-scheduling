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
        self.E = random.randint(1,5)
        self.D = random.randint(5,10)
        self.B = random.randint(1,10)

        self.I = self.E*self.B                # number of iterations
        self.r = time                         # release time
        self.Tasks = []
        self.t_c = np.random.rand(machines)
        self.t_s = np.random.rand(machines)
        self.weight = np.random.rand(1)[0]

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

