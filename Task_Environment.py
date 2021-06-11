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

        # DREAM parameter
        self.Middle_time = 0   # middle computation finish time
        self.Real_Allocate = 0
        self.Real_Start = 0
        self.Real_Complete = 0