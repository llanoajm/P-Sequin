# (DEPRECATED)

import random
from deap import base, creator, tools
from metrics import *
from utils import *


class NSGA:
    def __init__(self, initial_population, domain_appearances, strand_structures):
        
        self.initial_population = initial_population
        self.domain_appearances = domain_appearances
        self.strand_structures = strand_structures
        # Define the fitness and individual types inside the constructor
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0, -1.0)) # all metrics/objectives are to be minimized
        creator.create("Individual", list, fitness=creator.FitnessMulti, id=int) 
        
        self.toolbox = base.Toolbox()
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.variable_length_crossover)
        self.toolbox.register("mutate", self.mutate_sequence)
        self.toolbox.register("select", tools.selNSGA2)
    
    def evaluate(self, individual):
        strand = ''.join(individual)
        stability = compute_stability(strand)
        secondary_structures = check_secondary_structures(strand)
        lcs_value = 0  # Placeholder
        cross_hybridization = 0  # Placeholder
        palindrome_score = check_if_palindrome(strand)
        gc_content_score = check_gc_content(strand)
        return lcs_value, stability, secondary_structures, cross_hybridization, palindrome_score, gc_content_score

    def variable_length_crossover(self, parent1, parent2):
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

    def mutate_sequence(self, individual):
        mutation_point = random.randint(0, len(individual) - 1)
        available_bases = set(["A", "T", "C", "G"]) - {individual[mutation_point]}
        individual[mutation_point] = random.choice(list(available_bases))
        return individual,

    def run(self, generations):
        population = []
        id_counter = 0
        for strand in self.initial_population:
            ind = creator.Individual(strand)
            ind.id = id_counter
            id_counter += 1
            population.append(ind)

        # Evaluate the initial population
        fitnesses = list(map(self.toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # Run the genetic algorithm
        for gen in range(generations):
            offspring = self.toolbox.select(population, len(population))
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.7:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < 0.2:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            fitnesses = list(map(self.toolbox.evaluate, offspring))
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring

        # Sorting the final population by ID to retain original order
        population.sort(key=lambda x: x.id)
        
        return [''.join(ind) for ind in population]
    
    