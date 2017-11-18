import unittest

from neuroevolution import DiscreteGene
from neuroevolution import ContinuosGene
from neuroevolution import CategoricalGene
from neuroevolution import Chromosome
from neuroevolution import Dna
from neuroevolution import __crossover as recursiveCrossover
from neuroevolution import decide

chromosomes_fixture = [
        Chromosome(
            CategoricalGene('type', 'a', ['a', 'b']), 
            { DiscreteGene('gene-1-1', 1500), ContinuosGene('gene-1-2', 4000.550) }
            ),
        Chromosome(
            CategoricalGene('type', 'b', ['a', 'b']),
            { DiscreteGene('gene-2-1', 90), ContinuosGene('gene-2-2', 120.091) } 
            ),
        Chromosome(
            CategoricalGene('type', 'boo', ['foo', 'bar', 'boo']), 
            { ContinuosGene('gene-3-1', 50), ContinuosGene('gene-3-2', 8000.11) }
            ),
        Chromosome(
            CategoricalGene('type', 'b', ['a', 'b']),
            { CategoricalGene('gene-4-1', 'x', ['x', 'y', 'z', 'k']), DiscreteGene('gene-4-2', 10) } 
            )
        ]

class TestDecide(unittest.TestCase):
    
    def test_decide_to_mutate(self):
        gene = ContinuosGene('gene', 24631.473)
        mutated = decide(gene, 0.9998)
        self.assertTrue(gene != mutated)
        self.assertTrue(gene.get_name() == mutated.get_name())
        self.assertTrue(gene.get_value() != mutated.get_value())
        
    def test_decide_to_not_mutate(self):
        gene = ContinuosGene('gene', 24631.473)
        mutated = decide(gene, 0.000001)
        self.assertTrue(gene == mutated)
        self.assertTrue(gene.get_name() == mutated.get_name())
        self.assertTrue(gene.get_value() == mutated.get_value())


class TestBasicRecursiveCrossover(unittest.TestCase):
    
    def setUp(self):
        self.chromosomes = [
        Chromosome(
            CategoricalGene('type', 'a', ['a', 'b']), 
            { DiscreteGene('gene-1-1', 1500), ContinuosGene('gene-1-2', 4000.550) }
            ),
        Chromosome(
            CategoricalGene('type', 'b', ['a', 'b']),
            { DiscreteGene('gene-2-1', 90), ContinuosGene('gene-2-2', 120.091) } 
            ),
        Chromosome(
            CategoricalGene('type', 'boo', ['foo', 'bar', 'boo']), 
            { ContinuosGene('gene-3-1', 50), ContinuosGene('gene-3-2', 8000.11) }
            ),
        Chromosome(
            CategoricalGene('type', 'b', ['a', 'b']),
            { CategoricalGene('gene-4-1', 'x', ['x', 'y', 'z', 'k']), DiscreteGene('gene-4-2', 10) } 
            )
        ]

    def test__crossover(self):
        xs1 = [ self.chromosomes[0], self.chromosomes[1] ]
        xs2 = [ self.chromosomes[2], self.chromosomes[3] ]
        result = recursiveCrossover(xs1, xs2, 0, True, [], 0.0)
        for x in result:
            print(x)
        
if __name__ == '__main__':
    unittest.main()