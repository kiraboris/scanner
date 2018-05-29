
from copy import deepcopy

from scipy.optimize import differential_evolution

from pickett import experiment
from pickett.specunits import units
from pickett import rotor

import spec_compare


folder = "/home/borisov/Dropbox/astro_cologne/work/VinylCyanide/global/"

# calc test
myrotor = rotor.Rotor("VinylCyanide")
myrotor.mu_A = 3.815
myrotor.mu_B = 0.894
myrotor.add_param("A", value=4.985069674402932E+004)
myrotor.add_param("B", value=4.971163651218108E+003)
myrotor.add_param("C", value=4.513877260055734E+003)
myrotor.add_param("-DK", value=-2.714879748949775E+000)
myrotor.add_param("-DJK", value=8.501577850572951E-002)
myrotor.add_param("-DJ", value=-2.182401412532294E-003)

print("Rotor created")

myrotor.simulate(folder=folder)

print("Simulation complete")

input()


expname = "survey_peaks_raw.txt"

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
