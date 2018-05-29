
import lmfit.lineshapes as lineshapes
import bisect
import numpy as np

def add_gauss(xxx, yyy, line, sigma):
    
    index_left  = bisect.bisect_left(xxx, line.freq - 5 * sigma)
    index_right = bisect.bisect_left(xxx, line.freq + 5 * sigma)
    
    peak = lineshapes.gaussian(x=xxx[index_left:index_right], 
                               center=line.freq, sigma=sigma,
                               amplitude=np.sqrt(2*np.pi)*max(1.e-15, sigma))
    
    yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], peak)
    
                               
def add_impulse(xxx, yyy, line, sigma):

    index_left  = bisect.bisect_left(xxx, line.freq - sigma)
    index_right = bisect.bisect_left(xxx, line.freq + sigma)
    
    peak = np.ones(xxx[index_left:index_right].shape)
    yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], peak)


def make_grid(freq_limits, resolution):
    
    freq_min, freq_max = freq_limits
    
    return np.arange(freq_min, freq_max, resolution)

def make_spectrum(linelist, sigma_MHz, xxx, 
                  add_peak_function=add_impulse):
    
    yyy = np.zeros(xxx.shape)
    
    for line in linelist:
        add_peak_function(xxx, yyy, line, sigma_MHz)
        
    return yyy
    

def loss_product_impulse(exp, calc):
    
    return sum(np.logical_or(exp, calc))
    

def sigmoid(x):
    
    return 1.0 / (1.0 + np.exp(-x))   

def cross_loss(linelist_calc, linelist_exp, distance_transform_function=np.log):
    
    loss = -len(linelist_exp)*len(linelist_calc)

    for line_exp in linelist_exp:
        for line_calc in linelist_calc:
            distance = abs(line_calc.freq - line_exp.freq) 
            loss += sigmoid(distance)
            
    return loss
    
