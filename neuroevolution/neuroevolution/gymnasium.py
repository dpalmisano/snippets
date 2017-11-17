import logging
import math

from keras import backend as K

from .synthesis import Mitochondrion
from .evolution import party


class ModelPerformance:
    def __init__(self, dna, model, performance):
        self.dna = dna
        self.model = model
        self.performance = performance
    
    def __str__(self):
        return '[{}, {}, {}]'.format(self.dna, self.model, self.performance)

class Gymnasium:
    
    def __init__(self, train, test, initial_population_size = 100, logging_level = logging.DEBUG):
        self.train = train
        self.test = test
        self.initial_population_size = initial_population_size
        logging.basicConfig(level=logging_level)
        
    def __infer_maximum_number_of_layers__(self):
        return 3
        
    def __train_and_rank__(self, population):
        def mean_squared_error(y_true, y_pred):
            return K.square(y_true - y_pred)
        
        performances = []
        for idx, individual in enumerate(population):
            logging.info('Training individual {}/{}'.format(idx + 1, len(population)))
            model = Mitochondrion.synthesis(individual, 1, 1)
            model.compile(loss=mean_squared_error, optimizer='sgd')
            model.fit(self.train['x'].as_matrix(), self.train['y'].as_matrix(), verbose=0, epochs=20, batch_size=8)
            evaluation = model.evaluate(self.test['x'].as_matrix(), self.test['y'].as_matrix(), verbose=0, batch_size=8)
            performances.append(ModelPerformance(individual, model, evaluation))
        performances = [perf for perf in performances if math.isnan(perf.performance) == False]
        performances.sort(key=lambda x: x.performance, reverse=False)
        return performances
    
    def __natural_selection__(self, perfs, best_ratio = 0.30, worst_ratio = 0.10):
        best_size = round(len(perfs) * best_ratio)
        worst_size = round(len(perfs) * worst_ratio) if round(len(perfs) * worst_ratio) is not 0 else 1
        return perfs[:best_size] + perfs[-worst_size:]
        
    def start(self):
        max_number_of_layers = self.__infer_maximum_number_of_layers__() 
        logging.info('Generating initial random population of size {}'.format(self.initial_population_size))
        population = Mitochondrion.random_population(
            self.initial_population_size,
            max_number_of_layers)
    
        for i in range(5):
            logging.info('Evolution era {}/{}'.format(i,5))
            performances = self.__train_and_rank__(population)
            logging.info('Applying evolutionary pressure')
            performances = self.__natural_selection__(performances)
            logging.info('Most performant individual: {}'.format(performances[0].performance))
            population = [perf.dna for perf in performances]
            logging.info('Survivors are going to breed...')
            population = party(population)
        return population
        
