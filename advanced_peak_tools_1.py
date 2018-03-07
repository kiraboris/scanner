
import matplotlib.pyplot as plt
import numpy as np
import sys

from bisect import bisect_left
import lmfit.models as lmfit_models

from basetypes import Ranges, Units, DIM 

def step_and_span(settings):
    
    step = settings.max_fwhm.to(settings.data_units).magnitude 
        
    span = 4.0 * settings.max_fwhm.to(settings.data_units).magnitude
    
    return step, span
    
def accept_peak(peak, settings):
    """fidelity test for peak candidates"""
    
    flag1 = (peak.params['height'] >= settings.min_height)

    flag2 = (peak.params['fwhm'] >=
        settings.min_fwhm.to(settings.data_units).magnitude)
        
    flag3 = (peak.params['fwhm'] <=
        settings.max_fwhm.to(settings.data_units).magnitude)
        
    # candidate has a maximum
    flag4 = (peak.xxx[0] < peak.params['center'] < peak.xxx[-1])
        
    return flag1 and flag2 and flag3 and flag4

def converged_peak(peak):
    return peak.ier in range(1, 5)  
    # see https://docs.scipy.org/doc/scipy/reference/
    #    generated/scipy.optimize.leastsq.html 


def find_peaks(data_ranges, settings, fev_per_epoch = 16, nepochs=4):
    
    peak_model = lmfit_models.PseudoVoigtModel()     # TODO: derivatives
    local_baseline_model = lmfit_models.LinearModel()
    biased_peak_model = peak_model + local_baseline_model
    
    nslices = data_ranges.nslices(*step_and_span(settings), dim=DIM.X, nmipmap=2)
    slices  = data_ranges.slices(*step_and_span(settings), dim=DIM.X, nmipmap=2)

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
        scipy_leastsq_sett = {
            'maxfev': fev_per_epoch,
            'ftol':   1e-5,
            'xtol':   1e-5,
        }

        for n in range(0, nepochs):
            fit_out = biased_peak_model.fit(yyy, params, x = xxx,
                                            fit_kws = scipy_leastsq_sett)
            fit_out.xxx = xxx
            params = fit_out.params
            if converged_peak(fit_out): 
                break
            if not accept_peak(fit_out, settings):
                break

        # result of peak guess and fit
        if accept_peak(fit_out, settings):
            fit_out.xxx = xxx + offset
            fit_out.params['center'].value += offset
            peaklist.append(fit_out)
                                
        print("%3.1f%%" % (float(i) / float(nslices) * 100.0), end='\r')
        sys.stdout.flush()
        
    return peaklist
        


def peak_value(peak, flag_area = False):
    
    if not flag_area:
        return peak.params['height']
    else:
        return peak.params['height'] * peak.params['fwhm']

def extract_peaks(peaklist, xxx, flag_area = False):
    
    calc_x    = np.linspace(xxx[0], xxx[-1], num = 2 * len(xxx))
    calc_y    = np.zeros(calc_x.shape)
    calc_ny_t = np.zeros(calc_x.shape)
    calc_ny   = np.zeros(calc_x.shape)
    
    for p in peaklist:
        index = bisect_left(calc_x, p.params['center'])
        
        if index <= 0 or index >= len(calc_x) - 1:
            continue
        
        calc_ny_t[index] += 1
        ny_i = calc_ny[index] + 1
        y_i  = calc_y[index] + peak_value(p, flag_area)
        
        if calc_ny_t[index] >= calc_ny_t[index+1] and calc_ny_t[index] >= calc_ny_t[index-1]:
            di = 0
        elif calc_ny_t[index+1] >= calc_ny_t[index] and calc_ny_t[index+1] >= calc_ny_t[index-1]:
            di = +1
        else:
            di = -1
            
        calc_y[index-1:index+2] = 0 
        calc_ny[index-1:index+2] = 0
        
        calc_y[index+di] = y_i
        calc_ny[index+di] = ny_i 
    
    for i in range(0, len(calc_x)):
        if calc_ny[i] > 0:
            calc_y[i] = calc_y[i] / calc_ny[i]
    
    return calc_x, calc_y


def test():
    """test example for emission spectra"""
    
    units = Units.spec_units()
    
    class LineProfileSettings: pass
    settings = LineProfileSettings() 
    settings.data_units       = units.GHz
    settings.min_fwhm         = 0.08 * units.MHz
    settings.max_fwhm         = 1.5 * units.MHz
    settings.min_height       = 0.0008
    settings.derivative_order = 0
    
    folder = "/home/borisov/projects/work/emission/advanced/"
    filename = folder + '340K_norm_mean_spec.txt' # 'avg55_baseline.txt'
    
    data = np.loadtxt(filename)[6000:6500, :]
    
    # artificial baseline
    #data[:, 1] += 0.1* np.sin(data[:, 0]*3)
    
    data_ranges = Ranges(arrays=[data])
    
    peaklist = find_peaks(data_ranges, settings)
    
    xxx = data[:, 0]
    obs = data[:, 1]
    calc_x, calc_y = extract_peaks(peaklist, xxx, flag_area = False)
        
    f1 = plt.figure(figsize=(11.69,8.27))
    ax1 = f1.add_subplot(211)
    ax2 = f1.add_subplot(212)
    
    ax1.set_xlabel(r"Frequency [GHz]")
    ax1.set_ylabel(r"Intensity [arb]")
    ax2.set_xlabel(r"Frequency [GHz]")
    ax2.set_ylabel(r"Peak intensity [arb]")
    ax1.ticklabel_format(axis='x', useOffset=False)
    ax2.ticklabel_format(axis='x', useOffset=False)
    
    ax1.plot(xxx, obs,  color = 'k', lw=1)
    ax2.plot(calc_x, calc_y, color = 'b', lw=1)
    for p in peaklist: 
        ax1.plot(p.xxx, p.best_fit, color = 'r', lw=2)

    plt.savefig(folder+'test.png', papertype = 'a4', orientation = 'landscape')
    plt.close()
    
    
if __name__ == '__main__':
    test()
