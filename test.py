
import numpy as np
import lmfit.lineshapes as lineshapes
import matplotlib.pyplot as plt
import bisect

from pickett import experiment
from pickett.specunits import units
from pickett import simple_io


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


def make_spectrum(linelist, resolution, sigma_MHz, freq_limits_MHz, 
                  add_peak_function = add_impulse):
    
    freq_min, freq_max = freq_limits_MHz
    
    xxx = np.arange(freq_min, freq_max, resolution)
    yyy = np.zeros(xxx.shape)
    print(np.stack((xxx, yyy)).T.shape)
    
    for line in linelist:
        add_peak_function(xxx, yyy, line, sigma_MHz)
        
       
    return np.stack((xxx, yyy)).T
    

folder = "/home/borisov/projects/work/VinylCyanide/"

expname = "lines_exp1.txt"
calcname = "lines_calc_quotes.txt"

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
#exp.lines = exp.filter_lines(exp.lines, threshold=2.5)
#exp.save_lines(folder + 'lines_exp1.txt', 'simple')
#print('Saved')
#input()

limits = ((30, 70) * units.GHz).to(units.MHz).magnitude
sigma = settings.max_fwhm.to(units.MHz).magnitude
resolution = settings.min_fwhm.to(units.MHz).magnitude

print(limits)
print(sigma)
print(resolution)

spec_exp = make_spectrum(exp_lines, resolution, sigma, limits)
spec_calc = make_spectrum(calc_lines, resolution, sigma, limits)

f1 = plt.figure(figsize=(11.69,8.27))
ax1 = f1.add_subplot(111)

ax1.set_xlabel(r"Frequency [GHz]")
ax1.set_ylabel(r"Normalized")
ax1.ticklabel_format(axis='x', useOffset=False)

ax1.plot(spec_calc[:, 0], spec_calc[:, 1],  color = 'r', lw=2)
ax1.plot(spec_exp[:, 0], spec_exp[:, 1],  color = 'b', lw=2)
plt.show()
