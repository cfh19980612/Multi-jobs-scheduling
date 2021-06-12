import random
import matplotlib.pyplot as plt
import operator
import copy
from LP import *
# Function to generate a valid seating arrangement
def generatePermutation(Num_of_Jobs, Num_of_Machines, Jobs):
    length = 0
    for i in range (Num_of_Jobs):
        length += Jobs[i].D * Jobs[i].I
    Random_allocation = np.random.randint(0,Num_of_Machines,length)

    return Random_allocation

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
    solution1 = population[random.randint(0,size-1)]
    solution2 = population[random.randint(0,size-1)]
    
    # Apply tournament selection method to select parent
    r = random.uniform(0,1)
    if r<0.7:
        if solution1[1]>solution2[1]:
            return solution1[0] 
        else:
            return solution2[0]
    else:
        if solution1[1]>solution2[1]:
            return solution2[0] 
        else:
            return solution1[0]

# Crossover function to generate two childs
def crossover(parent1,parent2):
    length = len(parent1)

    # Randomly generate a crossover point
    cp = random.randint(0,length-1)

    # Generate offsprings by Horizontal Substring Crossover Method
    child1 = []
    for j in range(cp+1):
        child1.append(parent1[j])
    for j in range(cp+1,length):
        child1.append(parent2[j])

    child2 = []
    for j in range(cp+1):
        child2.append(parent2[j])
    for j in range(cp+1,length):
        child2.append(parent1[j])

    # Return generated offsprings
    return (child1,child2)

# Function to perform mutation
def mutate(individual):
    length = len(individual)

    for i in range (20):  # the number of mutation
    # Choose 2 points randomly and swap their values
        idx = random.randint(0,length-1)
        i = idx//length
        j = idx%length

        individual[i],individual[j] = individual[j],individual[i]

# Function to check if a solution is valid permuation of integers or not
def checkSolution(individual,persons):
    # Calculate frequency of occurence of each person
    freq = [0]*persons
    for row in individual:
        for val in row:
            freq[val-1] += 1

    for i in range(persons):
        if freq[i]!=1:
            return False    
    return True

def ga(Num_of_Jobs, Num_of_Machines, Jobs):
    LP = DLJS_LP(Jobs, Num_of_Jobs, Num_of_Machines)
    # Define variables
    X = []
    Y = []
    best = []
    bestLP = []
    bestFitness = 1000000

    # Define parameters
    POP_SIZE = 50  # size of the population
    NO_GEN = 100   # number of generations
    MUTATION_PROB = 0.9   # probability of mutation
    CROSS_PROB = 0.9

    # Generate initial population
    population = generateInitialPopulation(POP_SIZE, Num_of_Jobs, Num_of_Machines, Jobs)
    weightedPopulation = []

    # Loop through number of generations
    for generation in range(NO_GEN):
        weightedPopulation.clear()

        # Calculate ftiness of each individual in current population and store
        for individual in population:
            lp_solution, fitness = LP.LP_Solver(individual)
            new_ind = copy.deepcopy(individual)
            weightedPopulation.append((new_ind,fitness,lp_solution))

        # Store population in descending order of fitness
        weightedPopulation.sort(key=operator.itemgetter(1),reverse=False)

        population.clear()

        # Send top 10% solutions to the next generation without any change (Elitism)
        for i in range(POP_SIZE//5):
            new_list = copy.deepcopy(weightedPopulation[i][0])
            population.append(new_list)

        # Fill the rest of the population from the current mating pool
        while len(population)<POP_SIZE:
            # Select 2 parent for mating
            parent1 = selectParent(weightedPopulation)
            parent2 = selectParent(weightedPopulation)

            # Do crossover to generate offsprings
            child1,child2 = crossover(parent1,parent2)
            
            # Mutate offsprings with probability = MUTATION_PROB
            k = random.uniform(0,1)
            if k<MUTATION_PROB:
                mutate(child1)
                mutate(child2)

            # If offsprings generated are valid, add it to population for next generation
            population.append(child1)

            population.append(child2)

        # Print best solution from current generation
        currBestSolution = weightedPopulation[0][0]
        currBestFitness = weightedPopulation[0][1]
        currBestLP = weightedPopulation[0][2]
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
    print()
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
