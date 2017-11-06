class Gene:
    
    def __init__(self, gene_type, base, features):
        self.gene_type = gene_type
        self.base = base
        self.features = features
    
    def binary(self):
        gene_type_bin = bin(self.base.index(self.gene_type))
        return gene_type_bin[2:].zfill(len(self.base).bit_length())
    
    def __str__(self):
        return "[{},{},{}]".format(self.gene_type, self.features, self.binary())

class Chromosome:
    
    def __init__(self):
        self.genes = []
        
    def __init__(self, genes):
        self.genes = genes
        
    def add(self, gene):
        self.genes.append(gene)
    
    def get_genes(self):
        return self.genes
        
    def __str__(self):
        return ' -> '.join([str(g) for g in self.genes])

def pick(x1, x2, index, switch):
    if(switch):
        val = x1[index]
        if(val != None):
            return val
        else:
            return x2[index]
    else:
        val = x2[index]
        if(val != None):
            return val
        else:
            return x1[index]

def breed(chromosome1, chromosome2):
    return { 
        "child_1": Chromosome(crossover(chromosome1.get_genes(), chromosome2.get_genes(), True)),
        "child_2": Chromosome(crossover(chromosome1.get_genes(), chromosome2.get_genes(), False))
    }
        
def crossover(x1, x2, switch = True):
    if len(x1) > len(x2):
        x22 = ([None] * (len(x1) - len(x2))) + x2
        return __crossover(x1, x22, 0, switch, [])
    if len(x1) < len(x2):
        x11 = ([None] * (len(x2) - len(x1))) + x1
        return __crossover(x11, x2, 0, switch, [])
    return __crossover(x1, x2, 0, switch, [])

def __crossover(x1, x2, index, switch, result):
    if len(result) == len(x1):
        return result
    result.append(pick(x1, x2, index, switch))
    return __crossover(x1, x2, index + 1, not switch, result)
