
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import differential_evolution

from pickett_old import experiment
from pickett_old.specunits import units
from pickett_old import rotor

import spec_compare


folder = "C:/Users/Kirill/Dropbox/astro_cologne/work/VinylCyanide/global/"

# calc test
myrotor = rotor.Rotor("VinylCyanide")
myrotor.mu_A = 3.815
myrotor.mu_B = 0.894
if 1:
    myrotor.add_param("A", value=4.985069674402932E+004)
    myrotor.add_param("B", value=4.971163651218108E+003)
    myrotor.add_param("C", value=4.513877260055734E+003)
    myrotor.add_param("-DK", value=-2.715879748949775E+000)
    myrotor.add_param("-DJK", value=8.501577850572951E-002)
    myrotor.add_param("-DJ", value=-2.182401412532294E-003)
else:
    myrotor.add_param("A", value=47150.1492008695)
    myrotor.add_param("B", value=4775.88459979234)
    myrotor.add_param("C", value=4775.87827374227)
    myrotor.add_param("-DK", value=5.74945433429925)
    myrotor.add_param("-DJK", value=2.44109314676401E-5)
    myrotor.add_param("-DJ", value=-0.14399564983054)


print("Rotor created")

expname = "peaks_pgopher.txt"

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

# TODO: make standard meaning for threshold parameter and GUI to find them
exp.lines = exp.filter_lines(exp.lines, threshold=1.5)


limits = ((80, 110) * units.GHz).to(units.MHz).magnitude
sigma = settings.avg_fwhm.to(units.MHz).magnitude
resolution = settings.min_fwhm.to(units.MHz).magnitude
sigma_factor = 5

xxx = spec_compare.make_grid(limits, resolution)

print("Searching for global minimum...")

# +++++++++
#myrotor.simulate(folder=folder, threshold=-5.0)
#spectrum_calc = spec_compare.make_spectrum(myrotor.sim_lines, sigma_MHz=sigma_factor* sigma, xxx=xxx)
#spectrum_exp = spec_compare.make_spectrum(exp.lines, sigma_MHz=sigma_factor * sigma, xxx=xxx)
#loss = spec_compare.product_impulse_loss(calc=spectrum_calc, exp=spectrum_exp)
#print(loss)
#sys.exit()
# +++++++++


def make_calc(params):

    for name, value in zip(param_names, params):
        myrotor.params[name].value = value
    myrotor.simulate(folder=folder, threshold=-5.0)
    return myrotor.sim_lines


def model_loss(params):

    debug_str = "Debug:"
    for name, value in zip(param_names, params):
        debug_str += " %s=%.4e" % (name, value)

    spectrum_calc = spec_compare.make_spectrum(make_calc(params), sigma_MHz=sigma_factor*sigma, xxx=xxx)
    spectrum_exp = spec_compare.make_spectrum(exp.lines, sigma_MHz=sigma_factor*sigma, xxx=xxx)

    loss = spec_compare.product_impulse_loss(calc=spectrum_calc, exp=spectrum_exp)
    print(debug_str + ": loss=%6d" % loss)
    return loss


# +++++++++++++++++++
param_names = ['A', 'B', 'C', '-DK', '-DJK', '-DJ']
param_ranges = [(4e+4, 6e+4), (4e+3, 6e+3), (4e+3, 6e+3), (-10, 10), (-1, 1), (-1, 1)]

result = differential_evolution(model_loss, param_ranges)

print(result.x, result.fun)
    

# [ 4.03991374e+04  4.00298660e+03  4.11410398e+03 -9.60547173e+00
#  -8.88802647e-02 -9.77538296e-01] -9581.0

#f1 = plt.figure(figsize=(11.69,8.27))
#ax1 = f1.add_subplot(111)


#ax1.set_xlabel(r"Frequency [MHz]")
#ax1.set_ylabel(r"Normalized")
#ax1.ticklabel_format(axis='x', useOffset=False)

#ax1.plot(spec_calc[:, 0], spec_calc[:, 1],  color = 'r', lw=2)
#ax1.plot(spec_exp[:, 0], spec_exp[:, 1],  color = 'b', lw=2)
#plt.show()
