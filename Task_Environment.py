import random
import numpy as np

class task:
    def __init__(self,job_id,iter_id,machines,t_c,t_s):
        super().__init__()
        self.job_id = job_id
        self.iter_id = iter_id
        self.t_c = t_c
        self.t_s = t_s
        self.Allocate = 0
        self.P = [0 for i in range (machines)]
