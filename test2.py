from scipy.optimize import differential_evolution

from old import experiment, rotor
from entities.specunits import units

import spec_compare


folder = "C:/Users/Kirill/Dropbox/astro_cologne/work/VinylCyanide/global/"

# calc test
myrotor = rotor.Rotor("VinylCyanide")
myrotor.mu_A = 3.815
myrotor.mu_B = 0.894
if 0:
    myrotor.add_param("A", value=4.985069674402932E+004)
    myrotor.add_param("B", value=4.971163651218108E+003)
    myrotor.add_param("C", value=4.513877260055734E+003)
    myrotor.add_param("-DK", value=-2.714879748949775E+000)
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

# +++++++++
#myrotor.simulate(folder=folder, threshold=-5.0)
#print(spec_compare.cross_loss(myrotor.sim_lines, exp.lines))
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

    loss = spec_compare.cross_loss(make_calc(params), exp.lines)
    print(debug_str + ": loss=%.2e" % loss)
    return loss


# +++++++++++++++++++
param_names = ['A', 'B', 'C', '-DK', '-DJK', '-DJ']
param_ranges = [(4e+4, 6e+4), (4e+3, 6e+3), (4e+3, 6e+3), (-10, 10), (-1, 1), (-1, 1)]

result = differential_evolution(model_loss, param_ranges)

print(result.x, result.fun)  

#[ 5.15251264e+04  4.37304298e+03  4.10605418e+03  4.87446578e+00
#  7.00734949e-02 -9.94712353e-01] -12.55019398376549

#f1 = plt.figure(figsize=(11.69,8.27))
#ax1 = f1.add_subplot(111)


#ax1.set_xlabel(r"Frequency [MHz]")
#ax1.set_ylabel(r"Normalized")
#ax1.ticklabel_format(axis='x', useOffset=False)

#ax1.plot(spec_calc[:, 0], spec_calc[:, 1],  color = 'r', lw=2)
#ax1.plot(spec_exp[:, 0], spec_exp[:, 1],  color = 'b', lw=2)
#plt.show()
