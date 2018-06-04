
import lmfit.lineshapes as lineshapes
import bisect
import numpy as np
from scipy.special import erf

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
    

def product_impulse_loss(exp, calc):
    
    return sum(np.logical_or(exp, calc))
    

def sigmoid(x):
    
    return 1.0 / (1.0 + np.exp(-x))   


def cross_loss(linelist_calc, linelist_exp, assign_freq_tol=1.5):

    # lines are sorted; a cutoff window could be introduced
    # simplest temporary assignment without preserving combinations (most left one inside window)

    loss = 0.0
    assigned_qids = set()
    for line_calc in linelist_calc:
        for line_exp in linelist_exp:
            distance = abs(line_calc.freq - line_exp.freq)
            importance = 1.0 - erf(distance / assign_freq_tol)

            if line_exp.assigned_line and line_exp.assigned_line.qid() in assigned_qids:
                if distance <= assign_freq_tol:
                    continue

            if distance <= assign_freq_tol:
                line_exp.assigned_line = line_calc
                assigned_qids.add(line_calc.qid())

            loss -= importance

    return loss
