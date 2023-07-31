import random
import string

# Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.7
MAX_GENERATIONS = 1000
STRING_LENGTH = 10
CHARSET = 'ACGT'

def random_string(length):
    return ''.join(random.choice(CHARSET) for _ in range(length))

def longest_common_substring(s1, s2):
    m = len(s1)
    n = len(s2)
    counter = [[0] * (n + 1) for x in range(m + 1)]
    longest = 0
    lcs_set = set()

    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(s1[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(s1[i-c+1:i+1])

    return longest

def fitness(individual, population):
    return sum(longest_common_substring(individual, other) for other in population)

def mutate(individual):
    index = random.randint(0, len(individual) - 1)
    return individual[:index] + random.choice(CHARSET) + individual[index+1:]

def crossover(parent1, parent2):
    index = random.randint(0, len(parent1) - 1)
    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    return child1, child2

def genetic_algorithm(n_best):
    population = [random_string(STRING_LENGTH) for _ in range(POPULATION_SIZE)]
    for generation in range(MAX_GENERATIONS):
        population.sort(key=lambda individual: fitness(individual, population))
        
        # If the fitness of the best individual is 0, stop
        if fitness(population[0], population) == 0:
            break

        next_population = population[:n_best]  # elitism: retain the n best individuals
        while len(next_population) < POPULATION_SIZE:
            if random.random() < CROSSOVER_RATE:
                parent1 = random.choice(population[:50])
                parent2 = random.choice(population[:50])
                child1, child2 = crossover(parent1, parent2)
                next_population.extend([child1, child2])
            else:
                next_population.append(random.choice(population))
        
        # Apply mutation
        for i in range(len(next_population)):
            if random.random() < MUTATION_RATE:
                next_population[i] = mutate(next_population[i])
        
        population = next_population

    population.sort(key=lambda individual: fitness(individual, population))
    return population[:n_best]

# Test
best_strings = genetic_algorithm(5)
print(best_strings)
