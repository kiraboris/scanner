
import numpy as np
import lmfit.lineshapes as lineshapes

from pickett import experiment
from pickett.specunits import units
from pickett import simple_io


def make_spectrum(linelist, resolution, sigma_MHz, freq_limits_MHz):
    
    freq_min, freq_max = freq_limits_MHz
    
    xxx = np.arange(freq_min, freq_max, resolution)
    yyy = np.zeros(xxx.shape)
    
    for i, x in enumerate(xxx):
        for line in linelist:
            if line.freq - 5 * sigma_MHz < x < line.freq + 5 * sigma_MHz:
                yyy[i] = max(yyy[i], lineshapes.gaussian(center=line.freq, sigma=sigma_MHz))
    
    return np.stack((xxx, yyy)).T
    

folder = "/home/borisov/projects/work/VinylCyanide/"

expname = "lines_exp.txt"
calcname = "lines_calc.txt"

class ExpSettings: pass
settings = ExpSettings() 
settings.data_units       = units.GHz
settings.min_fwhm         = 80  * units.kHz
settings.max_fwhm         = 250  * units.kHz
settings.step             = 750  * units.kHz
settings.nsigma           = 10
settings.peak_model       = "GaussDerivative"
settings.flag_verbose     = True

exp = experiment.Experiment(settings)

exp.load_lines(folder + expname, 'simple')

exp_lines = exp.lines
calc_lines = simple_io.load_lines(folder + calcname)


limits = ((30, 70) * units.GHz).to(units.MHz).magnitude
sigma = settings.step.to(units.MHz).magnitude
resolution = settings.min_fwhm.to(units.MHz).magnitude

spec_exp = make_spectrum(exp_lines, resolution, sigma, limits)


