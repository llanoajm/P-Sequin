import random
from utils import *
from deap import base, creator, tools

creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

def evaluate(individual):
    strand = ''.join(individual)
    stability = float(compute_stability(strand))
    secondary_structures = check_secondary_structures(strand)
    lcs_value = 0 # lcs not yet created. TODO: establish graph relationships
    cross_hybridization = 0 # c_h method not yet created. TODO: establish graph relationships
    return lcs_value, stability, secondary_structures, cross_hybridization

toolbox.register("evaluate", evaluate)

# :::

desired_lengths_quantities = { # take actual input from flask.
    10: 25,
    15: 30,
    20: 20,
    25: 25
}

population = []
for length, quantity in desired_lengths_quantities.items():
    toolbox.register("individual_{}".format(length), tools.initIterate, creator.Individual, lambda l=length: initialize_sequence(l))
    population.extend(toolbox.__getattribute__("individual_{}".format(length))() for _ in range(quantity))

def variable_length_crossover(parent1, parent2):
    if len(parent1) < len(parent2):
        shorter, longer = parent1, parent2
    else:
        shorter, longer = parent2, parent1
    # Determine the crossover point within the range of the shorter sequence.
    crossover_point = random.randint(0, len(shorter) - 1)
    # Create offspring
    offspring1 = longer[:len(longer) - len(shorter) + crossover_point] + shorter[crossover_point:]
    offspring2 = shorter[:crossover_point] + longer[len(longer) - len(shorter) + crossover_point:len(longer) - len(shorter) + len(shorter)]
    # Return offspring in the order of input parents
    if len(parent1) < len(parent2):
        return offspring2, offspring1
    else:
        return offspring1, offspring2
    
toolbox.register("mate", variable_length_crossover)

def mutate_sequence(individual):
    mutation_point = random.randint(0, len(individual) - 1)
    available_bases = set(["A", "T", "C", "G"]) - {individual[mutation_point]}
    individual[mutation_point] = random.choice(list(available_bases))
    return individual,

toolbox.register("mutate", mutate_sequence)
toolbox.register("select", tools.selNSGA2)

# Evaluate the entire initial population

fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit



n_generations = 1  # You can adjust this value as per your requirements

for gen in range(n_generations):
    # Select the next generation individuals
    offspring = toolbox.select(population, len(population))
    
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.7:  # 70% crossover probability; you can adjust this value
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:  # 20% mutation probability; you can adjust this value
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the offspring
    fitnesses = list(map(toolbox.evaluate, offspring))
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    # Replace the old population with the offspring
    population[:] = offspring


