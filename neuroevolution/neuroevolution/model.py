import random
from random import randint

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
        
    def __str__(self):
        return "[{},{}]".format(self.name, self.value)


class ContinuosGene(Gene):
    
    def __randomise(value):
        return value + random.uniform(-value/2, value/2)
    
    def __init__(self, name, value):
        Gene.__init__(self, name, value)
        
    def mutate(self):
        return ContinuosGene(self.name, ContinuosGene.__randomise(self.value))


class DiscreteGene(Gene):
    
    def __randomise(value):
        return value + randint(round(-value/2), round(value/2))
    
    def __init__(self, name, value):
        Gene.__init__(self, name, value)
    
    def mutate(self):
        return DiscreteGene(self.name, DiscreteGene.__randomise(self.value))
    

class CategoricalGene(Gene):
    
    def __init__(self, name, value, base):
        Gene.__init__(self, name, value)
        self.base = base
    
    def mutate(self):
        index = randint(0, len(self.base) - 1)
        return CategoricalGene(self.name, self.base[index], self.base)


class Chromosome:
        
    def __init__(self, allosome, genes):
        self.allosome = allosome
        self.genes = genes
        
    def add(self, gene):
        self.genes.add(gene)
    
    def get_genes(self):
        return self.genes.copy()
        
    def get_allosome(self):
        return self.allosome
        
    def mutate(self):
        x_genes = list(self.genes.copy())
        index_to_mutate = randint(0, len(self.genes) - 1)
        x_genes[index_to_mutate] = x_genes[index_to_mutate].mutate()
        return Chromosome(self.allosome, x_genes)
        
    def __str__(self):
        return str(self.allosome) + ','.join([str(g) for g in self.genes])
    
    def __eq__(self, other):
        return (self.allosome == other.allosome) and (self.genes == other.genes)
        
    def __hash__(self):
        return hash(frozenset(self.genes)) + hash(self.allosome)


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