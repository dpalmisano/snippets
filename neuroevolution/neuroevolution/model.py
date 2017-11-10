import random
from random import randint

from .utils import bin_to_float
from .utils import float_to_bin

class Gene:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def get_name(self):
        return self.name
        
    def get_value(self):
        return self.value
        
    def __hash__(self):
        return hash(self.name + str(self.value))

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


class ContinuosGene(Gene):
    
    def __randomise(value):
        return value + random.uniform(-value/2, value/2)
    
    def __init__(self, name, value):
        Gene.__init__(self, name, value)
        
    def mutate(self):
        return ContinuosGene(self.name, ContinuosGene.__randomise(self.value))

    def __str__(self):
        return "[{},{}]".format(self.name, self.value)


class DiscreteGene(Gene):
    
    def __init__(self, name, value, base):
        Gene.__init__(self, name, value)
        self.base = base
    
    def mutate(self):
        index = randint(0, len(self.base) - 1)
        return DiscreteGene(self.name, self.base[index], self.base)
    
    def __str__(self):
        return "[{},{}]".format(self.name, self.value)


class Chromosome:
        
    def __init__(self, genes):
        self.genes = genes
        
    def add(self, gene):
        self.genes.add(gene)
    
    def get_genes(self):
        return self.genes.copy()
        
    def mutate(self):
        x_genes = list(self.genes.copy())
        index_to_mutate = randint(0, len(self.genes) - 1)
        x_genes[index_to_mutate] = x_genes[index_to_mutate].mutate()
        return Chromosome(x_genes)
        
    def __str__(self):
        return ','.join([str(g) for g in self.genes])
    
    def __eq__(self, other):
        return self.genes == other.genes
        
    def __hash__(self):
        return hash(frozenset(self.genes))


class Dna:
    
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes
    
    def get_chromosomes(self):
        return self.chromosomes.copy()
        
    def __str__(self):
        return '[' + ' -> '.join([str(x) for x in self.chromosomes]) + ']'
    
    def __eq__(self, other):
        return self.chromosomes == other.chromosomes
        
    def __hash__(self):
        return hash(tuple(self.chromosomes))