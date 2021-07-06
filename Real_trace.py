import random
import numpy as np
from Task_Environment import *

class Real_job:
    def __init__(self,job_id,time,machines,tag):
        super().__init__()
        # self.E = random.randint(50,200)       # number of epoches
        # self.D = random.randint(5,100)        # number of chunks, i.e., number of tasks in each iteration
        # self.B = random.randint(10,100)       # number of mini-batches in each chunk

        # generate CV jobs
        if tag == 'CV':
            id = random.randint(1,3)
            if id == 1: # VGG16 on Cifar10 (E*100,B*100)
                self.E = 2
                self.D = 4
                self.B = 4
                temp = [100*0.008701996/self.D, 100*0.0101606/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'VGG16'
            elif id == 2: # ResNet50 on Cifar100 (E*100,B*100)
                self.E = 2
                self.D = 4
                self.B = 4
                temp = [100*0.072398903/self.D, 100*0.115064228/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'ResNet50'
            elif id == 3: # Inception V3 on Cifar100 (E*100,B*100)
                self.E = 2
                self.D = 4
                self.B = 15
                temp = [100*0.11686496/self.D, 100*0.1442247/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'Inception'
        # generate NLP jobs
        elif tag == 'NLP': # LSTM on PTB (E*100,B*100)
            id = random.randint(1,2) 
            if id == 1:
                self.E = 5
                self.D = 4
                self.B = 3
                temp = [100*0.098137448/self.D, 100*0.142886722/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'LSTM'
            elif id == 2: # Transformer on WMT16 (E*100,B*100)
                self.E = 4
                self.D = 4
                self.B = 5
                temp = [100*0.051147397/self.D, 100*0.114481531/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'Transformer'
        # generate Speech jobs
        # if tag == 'CV':
        #     id = random.randint(1,4)
        #     if id == 1:
        #         self.E = random.randint(1,3)
        #         self.D = random.randint(1,15)
        #         self.B = random.randint(1,3)
        #         self.t_c = 0.1 + np.random.randint(1, 6, machines)/100
        #         self.t_s = 0.1 + np.random.randint(6, 10, machines)/100
        #     elif id == 2:
        #         self.E = random.randint(1,3)
        #         self.D = random.randint(1,15)
        #         self.B = random.randint(1,3)
        #         self.t_c = 0.1 + np.random.randint(1, 6, machines)/100
        #         self.t_s = 0.1 + np.random.randint(6, 10, machines)/100
        #     elif id == 3:
        #         self.E = random.randint(1,3)
        #         self.D = random.randint(1,15)
        #         self.B = random.randint(1,3)
        #         self.t_c = 0.1 + np.random.randint(1, 6, machines)/100
        #         self.t_s = 0.1 + np.random.randint(6, 10, machines)/100
        # generate Rec. jobs
        elif tag == 'Rec':
            id = random.randint(1,2)
            if id == 1: # GraphSAGE on Cora (E*10,B*10)
                self.E = 2
                self.D = 4
                self.B = 2
                temp = [100*0.007415931/self.D, 100*0.0113888/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'GraphSAGE'
            elif id == 2: # FastGCN on Cora (E*10,B*10)
                self.E = 1
                self.D = 4
                self.B = 5
                temp = [100*0.002505484/self.D, 100*0.004263958/self.D]
                self.t_c = [temp[random.randint(0,1)] for j in range (machines)]
                self.t_s = [0.5 for i in range (machines)]
                self.type = 'FastGCN'
        ###########################################################

        self.I = self.E*self.B                # number of iterations
        self.r = time                         # release time
        self.Tasks = []
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
        print('Scale: ',self.D, self.I)

