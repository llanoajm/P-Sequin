import random
from deap import base, creator, tools
from metrics import *
from utils import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
        self.avg_fitness_over_generations = []
        

    def plot_fitness_over_generations(self):
        plt.plot(self.avg_fitness_over_generations)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Fitness Evolution Over Generations')
        plt.show()
        
    def evaluate(self, domain_individual):
        # Get the current sequence of the domain
        domain_sequence = ''.join(domain_individual)
        
        # Retrieve the IDs of the strands where this domain appears
        strand_ids = self.domain_appearances[domain_individual.id]
        
        
        num_metrics = 6  # Update this value to match the number of metrics you are using
        total_scores = [0] * num_metrics
        total_weight = 0
        
        # For each strand ID, reconstruct the strand using the current sequences of its constituent domains
        for strand_id in strand_ids:
            strand_structure = self.strand_structures[strand_id]
            
            # Determine the weight for this strand based on the number of distinct domain types to assign greater significance to domains that influence a strand's score more heavily.
            
            distinct_domain_types = set(domain_name.split("'")[0] for domain_name in strand_structure.split())
            weight = 1 / len(distinct_domain_types)

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
            weighted_scores = [score * weight for score in scores]
            total_scores = [sum(x) for x in zip(total_scores, weighted_scores)]
            total_weight += weight
        
    # Normalize by total weight
        if total_weight == 0:
            # Handle the special case here. You can return a default value or raise a specific exception.
            return (0, 0, 0, 0, 0, 0)  # Example default value
        average_scores = [score / total_weight for score in total_scores]
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
    def reconcile_complementary_domains(self, relevant_population):
        # Iterate through the domain names and sequences in pairs (assuming keys are paired with their complements)
        for domain_name, domain_sequence in list(relevant_population.items())[::2]:
            complement_name = domain_name + '*'  # Assuming complement names are appended with a prime symbol
            complement_sequence = relevant_population[complement_name]

            # Evaluate the domain and complement
            domain_individual = creator.Individual(list(domain_sequence))
            domain_individual.id = domain_name
            complement_individual = creator.Individual(list(complement_sequence))
            complement_individual.id = complement_name

            domain_score = sum(self.evaluate(domain_individual))
            complement_score = sum(self.evaluate(complement_individual))

            # Reconcile the sequences
            if domain_score > complement_score:  # If the domain is worse
                new_domain_sequence = compute_complement(complement_sequence)
                relevant_population[domain_name] = new_domain_sequence
            else:  # If the complement is worse
                new_complement_sequence = compute_complement(domain_sequence)
                relevant_population[complement_name] = new_complement_sequence




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
            # Calculate average fitness for this generation
            avg_fitness = sum(ind.fitness.values[0] for ind in relevant_population) / len(relevant_population)
            self.avg_fitness_over_generations.append(avg_fitness)

            
        for individual in relevant_population:
            self.initial_population[individual.id] = ''.join(individual)
            
        self.reconcile_complementary_domains(self.initial_population)

        # Reconstruct the final strands
        final_strands = []
        for strand_structure in self.strand_structures:
            strand = ''.join([self.initial_population[dom_name] for dom_name in strand_structure.split()])
            final_strands.append(strand)
        # Extract the evolved domain sequences
        evolved_domain_sequences = [{"name": domain_name, "sequence": sequence} for domain_name, sequence in self.initial_population.items()]
        
        
        return final_strands, evolved_domain_sequences