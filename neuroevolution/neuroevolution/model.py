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
    
    def from_binary(name, binary):
        return ContinuosGene(name, bin_to_float(binary))
    
    def __init__(self, name, value):
        Gene.__init__(self, name, value)
        
    def binary(self):
        return float_to_bin(self.value)
        
    def mutate(self):
        binary_list = list(self.binary())
        index_to_mutate = randint(0, len(binary_list) - 1)
        binary_list[index_to_mutate] = '0' if binary_list[index_to_mutate] == '1' else '1'
        return ContinuosGene.from_binary(self.name, ''.join(binary_list))

    def __str__(self):
        return "[{},{},{}]".format(self.name, self.value, self.binary())


class DiscreteGene(Gene):
    
    def from_binary(name, binary, base):
        return DiscreteGene(name, base[int(binary, 2)], base)
    
    def __init__(self, name, value, base):
        Gene.__init__(self, name, value)
        self.base = base
    
    def binary(self):
        value_bin = bin(self.base.index(self.value))
        return value_bin[2:].zfill(len(self.base).bit_length() - 1)
    
    def mutate(self):
        binary_list = list(self.binary())
        index_to_mutate = randint(0, len(binary_list) - 1)
        binary_list[index_to_mutate] = '0' if binary_list[index_to_mutate] == '1' else '1'
        index = int(''.join(binary_list), 2)
        return DiscreteGene(self.name, self.base[index], self.base)
    
    def __str__(self):
        return "[{},{},{}]".format(self.name, self.value, self.binary())


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