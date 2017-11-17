import random

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

from .model import Dna
from .model import CategoricalGene, DiscreteGene, ContinuosGene, Chromosome

class Mitochondrion:
    
    def __s(genes, name):
        return [gene for gene in genes if gene.get_name() == name][0]
    
    def __build_dense(units, activation, input_size = None):
        if input_size is None:
            return Dense(units, activation = activation)
        else:
            return Dense(units, activation = activation, input_dim = input_size)

    def __build_dropout(rate, input_size = None):
        if input_size is None:
            return Dropout(rate)
        else:
            return Dropout(rate, input_shape=(input_size,))


    def __dense(genes, input_size = None):
        return Mitochondrion.__build_dense(
            Mitochondrion.__s(genes, 'size').get_value(),
            Mitochondrion.__s(genes, 'activation').get_value(),
            input_size
        )
    
    def __dropout(genes, input_size = None):
        return Mitochondrion.__build_dropout(
            Mitochondrion.__s(genes, 'rate').get_value(),
            input_size
        )

    def __switch(layer_type, genes, input_size = None):
        if layer_type == 'Dense':
            return Mitochondrion.__dense(genes, input_size)
        elif layer_type == 'Dropout':
            return Mitochondrion.__dropout(genes, input_size)
        else:
            raise Exception(f'{layer_type} does not exists.')
    
    def __layer_synthesis(allosome, genes, input_size = None):
        return Mitochondrion.__switch(allosome.get_value(), genes, input_size)
    
    def synthesis(dna, input_size, output_size):
        model = Sequential()
        for x in dna.get_chromosomes():
            x_allosome = x.allosome
            if dna.get_chromosomes().index(x) == 0:
                layer = Mitochondrion.__layer_synthesis(x_allosome, x.get_genes(), input_size)
                model.add(layer)
            else:
                layer = Mitochondrion.__layer_synthesis(x_allosome, x.get_genes())
                try:
                    model.add(layer)
                except:
                    print(str(dna))
        model.add(Mitochondrion.__build_dense(1, 'linear'))
        return model
    
    def random_population(
        number_of_individuals,
        max_number_of_layers = 10,
        types_of_layers = ['Dense', 'Dropout'],
        activations = ['relu', 'sigmoid']
    ):
        
        individuals = []
        for i in range(number_of_individuals):
            number_of_layers = random.randint(1, max_number_of_layers)
            individual = Mitochondrion.random_individual(number_of_layers, types_of_layers, activations)
            individuals.append(individual)
        return individuals
    
    def random_individual(
        number_of_layers,
        types_of_layers,
        activations
    ):
        xs = []
        for i in range(0, number_of_layers):
            type_of_layer = random.choice(types_of_layers)
            x = Mitochondrion.random_x(type_of_layer, activations)
            xs.append(x)
        return Dna(xs)
    
    def random_x(type_of_layer, activations):
        if type_of_layer == "Dense":
            return Chromosome(CategoricalGene('type', type_of_layer, ['Dense', 'Dropout']), {
                CategoricalGene('activation', random.choice(activations), activations),
                DiscreteGene('size', random.randint(1, 200))
            })
        elif type_of_layer == "Dropout":
            return Chromosome(CategoricalGene('type', type_of_layer, ['Dense', 'Dropout']), {
                ContinuosGene('rate', random.random())
            })