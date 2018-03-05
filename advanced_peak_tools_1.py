
import matplotlib.pyplot as plt
from collections import namedtuple
import numpy as np
import sys

import pint
import lmfit
import lmfit.models as lmfit_models

from basetypes import Ranges


class LineProfileSettings: pass
    

def step_and_span(settings, step_nw =1.0, span_nw = 4.0):
    
    fwhm = settings.fwhm_estimate.to(settings.data_units).magnitude
    
    step = step_nw * fwhm
    span = span_nw * fwhm
    
    return step, span
    

def find_peaks(data, settings):
    
    data_ranges = Ranges(arrays=[data])
    
    # TODO: take account of derivatives
    peak_model = lmfit_models.PseudoVoigtModel()
    base_model = lmfit_models.LinearModel()
    model = peak_model + base_model
    
    peaklist = []
    print('Searching for peaks...')
    nslices = data_ranges.nslices(*step_and_span(settings), dim=0)
    slices  = data_ranges.slices(*step_and_span(settings), dim=0)
    
    for i, d in enumerate(slices):
        offset = d[0, 0]
        xxx = d[:, 0] - d[0, 0]
        yyy = d[:, 1]
                        
        params = peak_model.guess(yyy, x=xxx)
        params.add('intercept', value=0.0)
        params.add('slope', value=0.0)
        fit_out = model.fit(yyy, params, 
                            x=xxx, fit_kws={'maxfev': 50})
                            
        print("%i%%" % int(i / float(nslices) * 100), end='\r')
        sys.stdout.flush()
        
        if fit_out.params['height'] > np.std(yyy):
            fit_out.xxx = xxx + offset
            peaklist.append(fit_out)
        
    return peaklist, model
        

def test():
    # test example for emission spectra
    
    units = pint.UnitRegistry('units.txt')
    
    settings = LineProfileSettings() 
    
    settings.data_units       = units.GHz
    settings.fwhm_estimate    = 0.5 * units.MHz
    settings.derivative_order = 0
    
    folder = "/home/borisov/projects/work/emission/simple_model/"
    filename = folder + 'RT_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)[4000:6500, :]
    
    peaklist, model = find_peaks(data, settings)
    
    peaklist_sorted = sorted(peaklist, 
        key=lambda p: float(p.params['amplitude']), reverse=True)

    print('')         
    for p in peaklist_sorted:    
        print(float(p.params['amplitude']),float(p.params['center']) )
        
    f1 = plt.figure()
    ax1 = f1.add_subplot(111)
    ax1.plot(data[:, 0], data[:, 1], color = 'k', lw=1)
    for p in peaklist_sorted: 
        ax1.plot(p.xxx, p.best_fit, color = 'r', lw=2)

    plt.show()
    plt.close()
    
if __name__ == '__main__':
    test()
