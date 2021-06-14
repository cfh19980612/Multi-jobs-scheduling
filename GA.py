import random
import matplotlib.pyplot as plt
import operator
import copy
from LP_M import *
from DLJS_LP import *
# Function to generate a valid seating arrangement
def generatePermutation(Num_of_Jobs, Num_of_Machines, Jobs):
    length = 0
    for i in range (Num_of_Jobs):
        length += Jobs[i].D * Jobs[i].I
    random_m = np.random.randint(0,Num_of_Machines,length)
    m, x, fitness = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, random_m)

    return [m, x, fitness] 

# Function to generate initial population of size POP_SIZE
def generateInitialPopulation(POP_SIZE, Num_of_Jobs, Num_of_Machines, Jobs):
    population = []
    for i in range(POP_SIZE):
        population.append(generatePermutation(Num_of_Jobs, Num_of_Machines, Jobs))
    return population

# Function to calculate fitness of a solution
# Selection parent according to its fitness
def selectParent(population):
    size = len(population)

    # Randomly select 2 solutions from mating pool
    idx1 = random.randint(0,size-1)
    idx2 = random.randint(0,size-1)
    
    # Apply tournament selection method to select parent
    r = random.uniform(0,1)
    if r<0.7:
        if population[idx1][2]>population[idx2][2]:
            return population[idx1]
        else:
            return population[idx2]
    else:
        if population[idx1][2]>population[idx2][2]:
            return population[idx2]
        else:
            return population[idx1]

# Crossover function to generate two childs
def crossover(Num_of_Jobs, Num_of_Machines, Jobs, parent1,parent2):
    length = len(parent1[0])
    k = 20
    # Randomly generate a crossover point
    cp = random.randint(0,length-1)
    # Generate offsprings by Horizontal Substring Crossover Method
    child1 = []
    for j in range(cp+1):
        child1.append(parent1[0][j])
    for j in range(cp+1,length):
        child1.append(parent2[0][j])
    # for j in range(cp+k,length):
    #     child1.append(parent1[0][j])

    child2 = []
    for j in range(cp+1):
        child2.append(parent2[0][j])
    for j in range(cp+1,length):
        child2.append(parent1[0][j])
    # for j in range(cp+k,length):
    #     child2.append(parent2[0][j])

    # for i in range (length):
    #     if i % 2 == 0:
    #         child1.append(parent1[0][i])
    #         child2.append(parent2[0][i])
    #     else:
    #         child1.append(parent2[0][i])
    #         child2.append(parent1[0][i])

    child1_m, child1_x, child1_fit = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, child1)
    child2_m, child2_x, child2_fit = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, child2)
    # Return generated offsprings
    return [child1_m, child1_x, child1_fit], [child2_m, child2_x, child2_fit]

# Function to perform mutation
def mutate(Num_of_Jobs, Num_of_Machines, Jobs, individual):
    length = len(individual[0])

    # for i in range (length):
    #     idx = np.random.randint(0, Num_of_Machines, 1)
    #     individual[0][i] = (individual[0][i] + idx[0]) % Num_of_Machines

    for i in range (10):  # the number of mutation
    # Choose 2 points randomly and swap their values
        idx = random.randint(0,length-1)
        i = idx//length
        j = idx%length

        individual[0][i],individual[0][j] = individual[0][j],individual[0][i]
    mutate_m, mutate_x, mutate_fit = DLJS_solver(Num_of_Jobs, Num_of_Machines, Jobs, individual[0])
    return [mutate_m, mutate_x, mutate_fit]
# Function to check if a solution is valid permuation of integers or not
def checkSolution(Num_of_Jobs, Num_of_Machines, Jobs, individual):
    # Calculate frequency of occurence of each person
    length = 0
    for i in range (Num_of_Jobs):
        length += Jobs[i].D * Jobs[i].I
    if len(individual[0]) != length:
        print(len(individual[0]), length)
    else:
        return len(individual[0])

def ga(Num_of_Jobs, Num_of_Machines, Jobs):
    LP = LPM(Jobs, Num_of_Jobs, Num_of_Machines)
    # Define variables
    X = []
    Y = []
    best = []
    bestLP = []
    bestFitness = 1000000

    # Define parameters
    POP_SIZE = 10  # size of the population
    NO_GEN = 10   # number of generations
    MUTATION_PROB = 0.1   # probability of mutation
    CROSS_PROB = 0.9

    # Generate initial population
    population = generateInitialPopulation(POP_SIZE, Num_of_Jobs, Num_of_Machines, Jobs)

    weightedPopulation = []

    # Loop through number of generations
    for generation in range(NO_GEN):
        weightedPopulation.clear()

        # Calculate ftiness of each individual in current population and store
        for individual in population:
            # lp_solution, fitness = LP.LP_M_Solver(individual)
            new_ind = copy.deepcopy(individual[0])
            weightedPopulation.append([new_ind, individual[1], individual[2]])

        # Store population in descending order of fitness
        weightedPopulation.sort(key=operator.itemgetter(2),reverse=False)

        population.clear()

        # Send top 10% solutions to the next generation without any change (Elitism)
        for i in range(POP_SIZE//2):
            new_list = copy.deepcopy(weightedPopulation[i][0])
            population.append([new_list, weightedPopulation[i][1], weightedPopulation[i][2]])

        # Fill the rest of the population from the current mating pool
        while len(population)<POP_SIZE:
            # Select 2 parents' genetic for mating
            parent1 = selectParent(weightedPopulation)
            parent2 = selectParent(weightedPopulation)

            # check the solution
            checkSolution(Num_of_Jobs, Num_of_Machines, Jobs, parent1)
            checkSolution(Num_of_Jobs, Num_of_Machines, Jobs, parent2)

            # Do crossover to generate offsprings
            child1,child2 = crossover(Num_of_Jobs, Num_of_Machines, Jobs, parent1,parent2)
            
            # Mutate offsprings with probability = MUTATION_PROB
            k = random.uniform(0,1)
            if k<MUTATION_PROB:
                mutate(Num_of_Jobs, Num_of_Machines, Jobs, child1)
                mutate(Num_of_Jobs, Num_of_Machines, Jobs, child2)

            # If offsprings generated are valid, add it to population for next generation
            population.append(child1)

            population.append(child2)

        # Print best solution from current generation
        currBestSolution = weightedPopulation[0][0]
        currBestLP = weightedPopulation[0][1]
        currBestFitness = weightedPopulation[0][2]
        print("Generation", generation+1, ":", currBestFitness)

        # Store current best for graphical analysis
        X.append(generation+1)
        Y.append(currBestFitness)

        # Check if current best is better than best solution uptill now
        if currBestFitness<bestFitness:
            best = currBestSolution
            bestFitness = currBestFitness
            bestLP = currBestLP

    # Output best arrangement obtained after NO_GEN number of generations
    print("Best seating arrangement after",NO_GEN,"generations: ")
    print("With happiness score:",bestFitness)

    # Plot graph mapping generation with its corresponding best solution fitness
    # plt.plot(X,Y,'bo-')
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness Score')
    # plt.title('Best Fitness: %d' % bestFitness)
    # plt.show()
    # fig.savefig("/home/Multi_tasks_2022/Fig/GA.png")

    return bestLP, bestFitness
