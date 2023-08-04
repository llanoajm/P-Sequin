import random
from deap import base, creator, tools
from metrics import *
from utils import *

class NSGA:
    def __init__(self, initial_population, domain_appearances, strand_structures, domain_names):
        
        self.initial_population = dict(zip(domain_names, initial_population))
       
        self.domain_appearances = domain_appearances
        self.strand_structures = strand_structures
        
        # Define the fitness and individual types inside the constructor
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessMulti, id=str) 
        
        self.toolbox = base.Toolbox()
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", self.variable_length_crossover)
        self.toolbox.register("mutate", self.mutate_sequence)
        self.toolbox.register("select", tools.selNSGA2)

    
    def evaluate(self, domain_individual):
        # Get the current sequence of the domain
        domain_sequence = ''.join(domain_individual)
        
        # Retrieve the IDs of the strands where this domain appears
        strand_ids = self.domain_appearances[domain_individual.id]
        
        # For each strand ID, reconstruct the strand using the current sequences of its constituent domains
        total_scores = [0, 0, 0, 0, 0, 0]
        for strand_id in strand_ids:
            strand_structure = self.strand_structures[strand_id]

            reconstructed_strand = ''.join([self.initial_population[dom_name] for dom_name in strand_structure.split()])
            # Evaluate the performance of the reconstructed strand
            stability = compute_stability(reconstructed_strand)
            secondary_structures = check_secondary_structures(reconstructed_strand)
            lcs_value = 0  # Placeholder
            cross_hybridization = 0  # Placeholder
            palindrome_score = check_if_palindrome(reconstructed_strand)
            gc_content_score = check_gc_content(reconstructed_strand)
            
            # Combine the scores from all strands for an overall evaluation of the domain
            scores = [lcs_value, stability, secondary_structures, cross_hybridization, palindrome_score, gc_content_score]
            total_scores = [sum(x) for x in zip(total_scores, scores)]
        
        # Average the scores over all strands
        average_scores = [score / len(strand_ids) for score in total_scores]
        return tuple(average_scores)

    def variable_length_crossover(self, parent1, parent2):
        if len(parent1) < len(parent2):
            shorter, longer = parent1, parent2
        else:
            shorter, longer = parent2, parent1
        
        crossover_point = random.randint(0, len(shorter) - 1)
        offspring1_data = longer[:len(longer) - len(shorter) + crossover_point] + shorter[crossover_point:]
        offspring2_data = shorter[:crossover_point] + longer[len(longer) - len(shorter) + crossover_point:len(longer) - len(shorter) + len(shorter)]
        
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

        # Define the initial population
        population = [creator.Individual(list(sequence)) for domain_name, sequence in self.initial_population.items()]
        for domain_name, individual in zip(self.initial_population.keys(), population):
            individual.id = domain_name
        
        # Extract all domains from the population that appear in strands
        relevant_population = [individual for individual in population if self.domain_appearances[individual.id]]
        
        # Evaluate the relevant population
        fitnesses = list(map(self.toolbox.evaluate, relevant_population))
        for ind, fit in zip(relevant_population, fitnesses):
            ind.fitness.values = fit

        # Run the genetic algorithm using the filtered population
        for gen in range(generations):
            offspring = self.toolbox.select(relevant_population, len(relevant_population))
            
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
            
            relevant_population[:] = offspring
            
        for individual in relevant_population:
            self.initial_population[individual.id] = ''.join(individual)
            print(individual.id, " = ", individual)

        # Reconstruct the final strands
        final_strands = []
        for strand_structure in self.strand_structures:
            strand = ''.join([self.initial_population[dom_name] for dom_name in strand_structure.split()])
            final_strands.append(strand)
        # Extract the evolved domain sequences
        evolved_domain_sequences = [{"name": domain_name, "sequence": sequence} for domain_name, sequence in self.initial_population.items()]
        
        return final_strands, evolved_domain_sequences