import random
from utils import *
from deap import base, creator, tools

# Define the fitness and individual types
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti, id=int)  # Added an ID attribute

toolbox = base.Toolbox()

# Define the evaluation function
def evaluate(individual):
    strand = ''.join(individual)
    stability = float(compute_stability(strand))
    secondary_structures = check_secondary_structures(strand)
    lcs_value = 0  # Placeholder
    cross_hybridization = 0  # Placeholder
    return lcs_value, stability, secondary_structures, cross_hybridization

toolbox.register("evaluate", evaluate)

# Initialize the population
desired_lengths_quantities = {
    10: 25,
    15: 30,
    20: 20,
    25: 25
}

population = []
id_counter = 0
for length, quantity in desired_lengths_quantities.items():
    toolbox.register("individual_{}".format(length), tools.initIterate, creator.Individual, lambda l=length: initialize_sequence(l))
    for _ in range(quantity):
        ind = toolbox.__getattribute__("individual_{}".format(length))()
        ind.id = id_counter  # Assigning an ID
        id_counter += 1
        population.append(ind)

# Define the crossover function
def variable_length_crossover(parent1, parent2):
    if len(parent1) < len(parent2):
        shorter, longer = parent1, parent2
    else:
        shorter, longer = parent2, parent1
    
    crossover_point = random.randint(0, len(shorter) - 1)
    offspring1_data = longer[:len(longer) - len(shorter) + crossover_point] + shorter[crossover_point:]
    offspring2_data = shorter[:crossover_point] + longer[len(longer) - len(shorter) + crossover_point:len(longer) - len(shorter) + len(shorter)]
    
    # Create offspring as Individuals
    offspring1 = creator.Individual(offspring1_data)
    offspring2 = creator.Individual(offspring2_data)
    
    if len(offspring1) == len(parent1):
        offspring1.id = parent1.id
        offspring2.id = parent2.id
    else:
        offspring1.id = parent2.id
        offspring2.id = parent1.id
    
    return offspring1, offspring2

    
toolbox.register("mate", variable_length_crossover)

# Define the mutation function
def mutate_sequence(individual):
    mutation_point = random.randint(0, len(individual) - 1)
    available_bases = set(["A", "T", "C", "G"]) - {individual[mutation_point]}
    individual[mutation_point] = random.choice(list(available_bases))
    return individual,

toolbox.register("mutate", mutate_sequence)
toolbox.register("select", tools.selNSGA2)

# Evaluate the initial population
fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Run the genetic algorithm
n_generations = 2
for gen in range(n_generations):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.7:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    fitnesses = list(map(toolbox.evaluate, offspring))
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    population[:] = offspring

# Sorting the final population by ID to retain original order
population.sort(key=lambda x: x.id)

for ind in population:
    print(''.join(ind))