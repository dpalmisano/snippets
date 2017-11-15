import numpy as np

def random_fitting(start, end, size, fitting_function, err_interval, error = 'normal', ):
    x = np.linspace(start, end, size)
    delta = getattr(np.random, error)(-err_interval, err_interval, x.size)
    return (x, fitting_function(x) + delta)