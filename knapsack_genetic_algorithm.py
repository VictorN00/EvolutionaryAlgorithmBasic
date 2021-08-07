"""
knapsack genetic algorithm
author: Victor Nguyen
"""

import random
import numpy as np

# create bag w/ max wt
max_tot_wt = 3000

def create_item(min_wt, max_wt, min_val, max_val):
    return (random.randint(min_wt, max_wt), random.randint(min_val, max_val))

"""
def sum_wt(indiv):
    sum_wt = 0
    for i in range(len(indiv)):
        if indiv[i] == '1':
            sum_wt += items[i][0]
    return sum_wt

def sum_val(indiv):
    sum_val = 0
    for i in range(len(indiv)):
        if indiv[i] == '1':
            sum_val += items[i][1]
    return sum_val
"""

def fitness(indiv):
    sum_wt = 0
    sum_val = 0
    for i in range(len(indiv)):
        if indiv[i] == '1':
            sum_wt += items[i][0]
            sum_val += items[i][1]
    if sum_wt > max_tot_wt:
        return 0
    return sum_val

def crossover(parent1, parent2, crossover_pt):
    store1 = parent1
    parent1 = parent1[:crossover_pt + 1] + parent2[crossover_pt + 1:]
    parent2 = parent2[:crossover_pt + 1] + store1[crossover_pt + 1:]
    return (parent1, parent2)

def mutate(indiv, probability):
    pos = random.randrange(0, len(indiv))
    if random.random() < probability:
        indiv = list(indiv)
        if indiv[pos] == '0':
            indiv[pos] = '1'
        else:
            indiv[pos] = '0'
        indiv = ''.join(indiv)
    return indiv

def mutate_whole(pop, probability):
    for i in range(len(pop)):
        pop[i] = mutate(pop[i], probability)

# set number of items w/ weight and value
items = [create_item(50, 2500, 25, 1500) for i in range(10)]
print(items)

# create random genomes based on items
POPULATION_SIZE = 10
population = []
for i in range(POPULATION_SIZE):
    population.append(''.join(random.choice(['0', '1']) for i in range(len(items))))

max_gens = 25
for g in range(max_gens):
    # fitness
    population.sort(key=lambda x: fitness(x), reverse=True)
    print(population)
    print('best fitness = {}'.format(fitness(population[0])))
    # crossover
    new_population = []
    crossover_pt = random.randint(0, POPULATION_SIZE - 2)
    num_elites = max(1, int(0.2 * POPULATION_SIZE))
    if (POPULATION_SIZE - num_elites) % 2 == 1:
        num_elites += 1
    num_cross = POPULATION_SIZE - num_elites
    for i in range(num_cross // 2):
        # choose parents for crossover
        # possible probability method -> calculate total fitness of all combos, probability of being parent is proportion of that total fitness (can't crossover with itself)
        sum_fitness = sum([fitness(y) for y in population]) # might need to put this in []
        probabilities = None
        if sum_fitness > 0:
            probabilities = [fitness(x) / sum_fitness for x in population]
            if probabilities[1] == 0:
                probabilities[0] = 0.5
                probabilities[1:] = [0.5 / (POPULATION_SIZE - 1) for i in range(POPULATION_SIZE - 1)]
        par1 = np.random.choice([z for z in range(POPULATION_SIZE)], replace=False, p=probabilities)
        par2 = np.random.choice([z for z in range(POPULATION_SIZE)], replace=False, p=probabilities)
        child1, child2 = crossover(population[par1], population[par2], crossover_pt)
        new_population.append(child1)
        new_population.append(child2)
        
    # mutation
    mutate_whole(new_population, 0.5)
    
    # elitism (top few are copied directly)
    for i in range(num_elites):
        new_population.append(population[i])
        # print(population[i])
    
    # repeat fitness and child-making (prob have function for fitness, crossover, and mutation)
    population = new_population
    # population size should stay consistent, so this might be unnecessary
    POPULATION_SIZE = len(population)

population.sort(key=lambda x: fitness(x), reverse=True)
print(population)
print('best fitness = {}'.format(fitness(population[0])))
# could verify accuracy with dp algorithm
best = population[0]
print('best: ', best)
best_wt = 0
best_val = 0
for i in range(len(best)):
    if best[i] == '1':
        best_wt += items[i][0]
        best_val += items[i][1]
print('wt: ' + str(best_wt) + ' - val: ' + str(best_val))

"""
print()
print(population[0], population[1])
c1, c2 = crossover(population[0], population[1], 4)
print(c1, c2)
c1 = mutate(c1, 0.5)
print(c1)
"""

W = max_tot_wt
N = len(items)
dp = [[0 for x in range(W + 1)] for x in range(N + 1)]

for i in range(1, N + 1):
    for j in range(1, W + 1):
        if items[i - 1][0] > j:
            dp[i][j] = dp[i - 1][j]
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - items[i - 1][0]] + items[i - 1][1])

print('actual best value: ', dp[N][W])