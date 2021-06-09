import random
import numpy as np
from Job_Environment import *
from scipy.stats import binom

class Environment:
    def __init__(self, Num_of_machines, Num_of_jobs):
        super().__init__()
        self.Num_of_machines = Num_of_machines
        self.Num_of_jobs = Num_of_jobs
        self.release_time = np.random.binomial(10, 0.5, size = self.Num_of_jobs)
        self.Jobs = []
        for i in range (self.Num_of_jobs):
            self.Jobs.append(job(i,self.release_time[i],self.Num_of_machines))
    
    def Print_Env(self):
        for i in range(self.Num_of_jobs):
            self.Jobs[i].Print_job()
