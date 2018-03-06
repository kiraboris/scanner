
import matplotlib.pyplot as plt
import numpy as np
import sys

import lmfit.models as lmfit_models

from basetypes import Ranges, Units, DIM 


def step_and_span(settings, step_nw =2.0, span_nw = 4.0):
    
    step = step_nw * settings.min_fwhm.to(settings.data_units).magnitude
    span = span_nw * settings.max_fwhm.to(settings.data_units).magnitude
    
    return step, span
    

def find_peaks(data_ranges, settings, fev_per_epoch = 16, nepochs=8):
    
    peak_model = lmfit_models.PseudoVoigtModel()     # TODO: derivatives
    local_baseline_model = lmfit_models.LinearModel()
    biased_peak_model = peak_model + local_baseline_model
    
    nslices = data_ranges.nslices(*step_and_span(settings), dim=DIM.X)
    slices  = data_ranges.slices(*step_and_span(settings), dim=DIM.X)
    
    # fidelity test for peak candidates 
    def accept_peak(peak):
        flag1 = np.max(peak.best_fit) - np.min(peak.best_fit) > 2 * np.std(yyy)
        flag2 = (peak.params['fwhm'] > 
            settings.resolution.to(settings.data_units).magnitude)
            
        return flag1 and flag2
    
    def converged_peak(peak):
        return peak.ier in range(1, 5)  
        # see https://docs.scipy.org/doc/scipy/reference/
        #    generated/scipy.optimize.leastsq.html 

    peaklist = []    
    print('Searching for peaks...')
    for i, d in enumerate(slices):
        offset = d[0, 0]
        xxx = d[:, 0] - offset
        yyy = d[:, 1]
        
        # initital peak guess             
        params = peak_model.guess(yyy, x=xxx)
        params.add('intercept', value=0.0)
        params.add('slope', value=0.0)

        # peak fitting loop
        scipy_leastsq_settings = {
            'maxfev': fev_per_epoch,
            'ftol':   1e-5,
            'xtol':   1e-5,
        }

        for n in range(0, nepochs):
            fit_out = biased_peak_model.fit(yyy, params, x = xxx,
                                            fit_kws = scipy_leastsq_settings)
            params = fit_out.params
            if converged_peak(fit_out): 
                break
            if not accept_peak(fit_out):
                break

        
        # result of peak guess and fit
        if accept_peak(fit_out):
            fit_out.xxx = xxx + offset
            peaklist.append(fit_out)

                                
        print("%i%%" % int(i / float(nslices) * 100), end='\r')
        sys.stdout.flush()
        
    return peaklist
        

def test():
    """test example for emission spectra"""
    
    units = Units.spec_units()
    
    class LineProfileSettings: pass
    settings = LineProfileSettings() 
    settings.data_units       = units.GHz
    settings.min_fwhm         = 0.2 * units.MHz
    settings.max_fwhm         = 0.8 * units.MHz
    settings.resolution       = 70 * units.kHz
    settings.derivative_order = 0
    
    folder = "/home/borisov/projects/work/emission/simple_model/"
    filename = folder + 'RT_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)[4000:6500, :]
    
    data_ranges = Ranges(arrays=[data])
    
    peaklist = find_peaks(data_ranges, settings)
    
    
    # output
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
