import random
from itertools import combinations

from .model import Dna

def select(population):
    if len(population) < 4:
        return population
    else:
        return set(random.sample(population, 4))

def party(population):
    new_born = set({})
    for pair in combinations(population, 2):
        breed_result = breed(pair[0], pair[1], 0.0)
        new_born.add(breed_result['child_1'])
        new_born.add(breed_result['child_2'])
    return new_born

def evolve(initial_population, generations, select_function = select):
    for i in range(generations):
        population = select_function(initial_population)
        print(f'Generation: {i} - population size: {len(population)}')
        population.update(party(population))
    return population

def decide(g, mutation_probability):
    if(random.random() < mutation_probability):
        return g.mutate()
    else:
        return g

def pick(x1, x2, index, switch, mutation_probability):
    if(switch):
        val = x1[index]
        if(val is not None):
            return decide(val, mutation_probability)
        else:
            return decide(x2[index], mutation_probability)
    else:
        val = x2[index]
        if(val is not None):
            return decide(val, mutation_probability)
        else:
            return decide(x1[index], mutation_probability)

def breed(dna1, dna2, mutation_probability = 0.0):
    return { 
        "child_1": Dna(crossover(dna1.get_chromosomes(), dna2.get_chromosomes(), mutation_probability)),
        "child_2": Dna(crossover(dna1.get_chromosomes(), dna2.get_chromosomes(), mutation_probability, False))
    }
        
def crossover(x1, x2, mutation_probability, switch = True):
    if len(x1) > len(x2):
        x22 = ([None] * (len(x1) - len(x2))) + x2
        return __crossover(x1, x22, 0, switch, [], mutation_probability)
    if len(x1) < len(x2):
        x11 = ([None] * (len(x2) - len(x1))) + x1
        return __crossover(x11, x2, 0, switch, [], mutation_probability)
    return __crossover(x1, x2, 0, switch, [], mutation_probability)

def __crossover(x1, x2, index, switch, result, mutation_probability):
    if len(result) == len(x1):
        return result
    result.append(pick(x1, x2, index, switch, mutation_probability))
    return __crossover(x1, x2, index + 1, not switch, result, mutation_probability)