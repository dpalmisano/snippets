import unittest

from neuroevolution import ContinuosGene
from neuroevolution import DiscreteGene
from neuroevolution import CategoricalGene
from neuroevolution import Chromosome

class TestContinuosGene(unittest.TestCase):

    def setUp(self):
        self.initialValue = 44332.174
        self.gene = ContinuosGene('test-gene', self.initialValue)

    def test_mutate(self):
        mutated_gene = self.gene.mutate()
        self.assertTrue(mutated_gene != self.gene)
        self.assertTrue(mutated_gene.get_value() != self.gene.get_value())


class TestDiscreteGene(unittest.TestCase):
    
    def setUp(self):
        self.initialValue = 35382
        self.gene = DiscreteGene('test-gene', self.initialValue)
        
    def test_mutate(self):
        mutated_gene = self.gene.mutate()
        self.assertTrue(mutated_gene != self.gene)
        self.assertTrue(mutated_gene.get_value() != self.gene.get_value())


class TestCategoricalGene(unittest.TestCase):
    
    def setUp(self):
        self.initialValue = 'g'
        self.base = list("abcdefghijklmnopqrstuvwxyz")
        self.gene = CategoricalGene('test-gene', self.initialValue, self.base)
        
    def test_mutate(self):
        mutated_gene = self.gene.mutate()
        self.assertTrue(mutated_gene != self.gene)
        self.assertTrue(mutated_gene.get_value() != self.gene.get_value())


class TestChromosome(unittest.TestCase):
    
    def setUp(self):
        self.chromosome = Chromosome(
            CategoricalGene('type', 'a', ['a', 'b']),
            { DiscreteGene('gene-1', 72353), ContinuosGene('gene-2', 6634.242) }
            )
    
    def test_mutate(self):
        mutated_x = self.chromosome.mutate()
        self.assertTrue(mutated_x != self.chromosome)
        self.assertTrue(mutated_x.get_genes() != self.chromosome.get_genes())


if __name__ == '__main__':
    unittest.main()