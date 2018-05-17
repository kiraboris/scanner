
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import differential_evolution

from pickett import experiment
from pickett.specunits import units
from pickett import simple_io

import spec_compare


folder = "/home/borisov/InSync/astro_cologne/work/VinylCyanide/"

expname = "survey_peaks_raw.txt"
calcname = "survey_peaks_raw.txt"

class ExpSettings: pass
settings = ExpSettings() 
settings.data_units       = units.MHz
settings.min_fwhm         = 80  * units.kHz
settings.max_fwhm         = 350  * units.kHz
settings.avg_fwhm         = 200  * units.kHz
settings.nsigma           = 10.0
settings.peak_model       = "GaussDerivative"
settings.flag_verbose     = True

exp = experiment.Experiment(settings)
exp.load_lines(folder + expname, fileformat="simple")
exp.lines = exp.filter_lines(exp.lines, threshold=1.5)

#exp.save_lines(folder + 'lines_exp1.txt', 'simple')
#print('Saved')
#input()

limits = ((80, 110) * units.GHz).to(units.MHz).magnitude
sigma = settings.max_fwhm.to(units.MHz).magnitude
resolution = settings.min_fwhm.to(units.MHz).magnitude

xxx = spec_compare.make_grid(limits, resolution)

print("Searching for global minimum...")


def make_shifted_exp(exp, par_shift):
    
    lines = deepcopy(exp)
    for line in lines:
        line.freq = line.freq + par_shift
    
    return lines

def model_loss(par_shift):
    
    return spec_compare.cross_loss(make_shifted_exp(exp.lines, 
                                                    par_shift),
                                    exp.lines)


def callback(x0, **args):
    
    loss = model_loss(x0)
    print("Loss: " + str(loss))
    return (loss < 0)

# +++++++++++++++++++
result = differential_evolution(model_loss, [(-100, 100)], callback=callback)

print(result.x, result.fun)  
    

#f1 = plt.figure(figsize=(11.69,8.27))
#ax1 = f1.add_subplot(111)


#ax1.set_xlabel(r"Frequency [MHz]")
#ax1.set_ylabel(r"Normalized")
#ax1.ticklabel_format(axis='x', useOffset=False)

#ax1.plot(spec_calc[:, 0], spec_calc[:, 1],  color = 'r', lw=2)
#ax1.plot(spec_exp[:, 0], spec_exp[:, 1],  color = 'b', lw=2)
#plt.show()
