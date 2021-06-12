import gurobipy as gp
import numpy as np
import math
from gurobipy import GRB
from Job_Environment import *
from Task_Environment import *

class DLJS_LP:
    def __init__(self,Jobs, Num_of_Jobs, Num_of_Machines):
        super().__init__()
        self.Jobs = Jobs
        self.Num_of_Jobs = Num_of_Jobs
        self.Num_of_Machines = Num_of_Machines

    def LP_Solver(self, solution):
        Num_of_jobs = range(self.Num_of_Jobs)
        Num_of_machines = range(self.Num_of_Machines)

        # initial
        for i in range (self.Num_of_Jobs):
            for j in range (self.Jobs[i].I):
                for k in range (self.Jobs[i].D):
                    for l in range (self.Num_of_Machines):
                        self.Jobs[i].Tasks[j][k].P[l] = 0

        Result = [[[0 for k in range (self.Jobs[i].D)] for j in range (self.Jobs[i].I)] for i in range (self.Num_of_Jobs)]
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
            m = gp.Model("LP")
            m.setParam('OutputFlag', 0)

            # Create variables
            x = [None for i in range (self.Num_of_Jobs)]  # start time
            C = m.addVars(self.Num_of_Jobs, lb = 0, vtype = GRB.CONTINUOUS, name = 'x')  # completion time
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
                for j in range (self.Jobs[i].I):
                    for k in range (self.Jobs[i].D):
                        Result[i][j][k] = x[i][j,k].x

            return Result, m.objVal

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))

        except AttributeError:
            print('Encountered an attribute error')



# """
# Given the following function:
#     y = f(w1:w6) = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + 6wx6
#     where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7) and y=44
# What are the best values for the 6 weights (w1 to w6)? We are going to use the genetic algorithm to optimize this function.
# """ 
# def LP_GA(Jobs, Num_of_Jobs, Num_of_Machines):
#     LP = DLJS_LP(Jobs, Num_of_Jobs, Num_of_Machines)

#     fitness_function = LP.LP_Solver

#     num_generations = 100 # Number of generations.
#     num_parents_mating = 7 # Number of solutions to be selected as parents in the mating pool.

#     # To prepare the initial population, there are 2 ways:
#     # 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
#     # 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
#     sol_per_pop = 50 # Number of solutions in the population.
#     num_genes = 0
#     for i in range (Num_of_Jobs):
#         num_genes += Jobs[i].D * Jobs[i].I

#     init_range_low = 0
#     init_range_high = Num_of_Machines - 1

#     parent_selection_type = "sss" # Type of parent selection.
#     keep_parents = 7 # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.

#     crossover_type = "single_point" # Type of the crossover operator.

#     # Parameters of the mutation operation.
#     mutation_type = "random" # Type of the mutation operator.
#     mutation_percent_genes = 10 # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists or when mutation_type is None.

#     last_fitness = 0

#     # Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
#     ga_instance = pygad.GA(num_generations=num_generations,
#                         num_parents_mating=num_parents_mating, 
#                         fitness_func=fitness_function,
#                         sol_per_pop=sol_per_pop, 
#                         num_genes=num_genes,
#                         init_range_low=init_range_low,
#                         init_range_high=init_range_high,
#                         parent_selection_type=parent_selection_type,
#                         keep_parents=keep_parents,
#                         crossover_type=crossover_type,
#                         mutation_type=mutation_type,
#                         mutation_percent_genes=mutation_percent_genes)

#     # Running the GA to optimize the parameters of the function.
#     ga_instance.run()

#     # After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
#     ga_instance.plot_result()

#     # Returning the details of the best solution.
#     solution, solution_fitness, solution_idx = ga_instance.best_solution()
#     print("Parameters of the best solution : {solution}".format(solution=solution))
#     print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
#     print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

#     prediction = numpy.sum(numpy.array(function_inputs)*solution)
#     print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

#     if ga_instance.best_solution_generation != -1:
#         print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

#     # Saving the GA instance.
#     filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
#     ga_instance.save(filename=filename)

#     # Loading the saved GA instance.
#     loaded_ga_instance = pygad.load(filename=filename)
#     loaded_ga_instance.plot_result()