
import numpy as np
import lmfit.lineshapes as lineshapes
import matplotlib.pyplot as plt
import bisect

from pickett import experiment
from pickett.specunits import units
from pickett import simple_io


def make_spectrum(linelist, resolution, sigma_MHz, freq_limits_MHz):
    
    freq_min, freq_max = freq_limits_MHz
    
    xxx = np.arange(freq_min, freq_max, resolution)
    yyy = np.zeros(xxx.shape)
    print(np.stack((xxx, yyy)).T.shape)
    
    #for i, x in enumerate(xxx):
    #    for line in linelist:
    #        if line.freq - 5 * sigma_MHz < x < line.freq + 5 * sigma_MHz:
    #            yyy[i] = max(yyy[i], lineshapes.gaussian(x=x, center=line.freq, sigma=sigma_MHz))
    
    for line in linelist:
        index_left  = bisect.bisect_left(xxx, line.freq - 5 * sigma_MHz)
        index_right = bisect.bisect_left(xxx, line.freq + 5 * sigma_MHz)
        
#        print(index_left)
#        print(index_right)
#        print(len(yyy[index_left:index_right]))
#        print(len(lineshapes.gaussian(x=xxx[index_left:index_right],
#                                             center=line.freq, sigma=sigma_MHz)))
#        input()
        yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], 
                                                 lineshapes.gaussian(x=xxx[index_left:index_right],
                                                 center=line.freq, sigma=sigma_MHz))
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

#exp_lines = exp.filter_lines(exp.lines, threshold = 1.25)
exp_lines = exp.lines
calc_lines = simple_io.load_lines(folder + calcname)


limits = ((30, 70) * units.GHz).to(units.MHz).magnitude
sigma = settings.step.to(units.MHz).magnitude
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
