
import matplotlib.pyplot as plt
import numpy as np
import bisect
import sys

import lmfit.models as lmfit_models
from boltzmann import lmfit_custom_models

from simulation.ranges import Ranges
from entities.specunits import units


def step_and_span(settings):
    
    step = 2 * settings.avg_fwhm.to(settings.data_units).magnitude
        
    span = 3 * step
    
    return step, span
    
    
def accept_peak(peak, settings):
    """fidelity test for peak candidates"""
    xxx = peak.xxx
    yyy = peak.yyy    

    # line width not extreme
    flag1 = (peak.params['fwhm'] >=
        settings.min_fwhm.to(settings.data_units).magnitude)
        
    flag2 = (peak.params['fwhm'] <=
        settings.max_fwhm.to(settings.data_units).magnitude)
    
    # candidate has a maximum
    flag3 = (xxx[0] < peak.params['center'] < xxx[-1])
    
    flag3a = True
    #if settings.peak_model == "GaussDerivative":
        # candidate also has at least one minumum
    #    flag3a = any([peak.best_fit[i-1] > peak.best_fit[i] and 
                    #peak.best_fit[i+1] > peak.best_fit[i] for
    #                  i in range(1, len(xxx)-1)])
    
    if not flag1 or not flag2 or not flag3 or not flag3a:
        return False
    
    # slope not extreme
    block_height = max(yyy) - min(yyy)
    block_width = xxx[-1] - xxx[0]
    flag4 = (peak.params['slope'] <= block_height / block_width)
    
    # line height positive and greater than noise height
    yyy_noise = yyy - peak.best_fit
    min_height_estimate = settings.nsigma * np.std(yyy_noise)    
    flag5 = (peak.params['height'] >= min_height_estimate)
    
    if not flag4 or not flag5:
        return False
    
    return True


def converged_peak(peak):
    return peak.ier in range(1, 5)  
    # see https://docs.scipy.org/doc/scipy/reference/
    #    generated/scipy.optimize.leastsq.html 


def eval_local_baseline(peak):
    
    local_baseline_model = lmfit_models.LinearModel()
    params = local_baseline_model.make_params()
    params['intercept'].set(value = peak.params['intercept']) 
    params['slope'].set(value = peak.params['slope'])   

    return local_baseline_model.eval(params, x=peak.xxx)


def make_peak_model(settings):
    
    if settings.peak_model == "GaussDerivative":
        return lmfit_custom_models.GaussDerivativeModel()
    elif settings.peak_model == "Voigt": 
        return lmfit_models.PseudoVoigtModel()
    else:
        return lmfit_models.GaussianModel()

def find_peaks(data_ranges, settings, fev_per_epoch = 16, nepochs = 4, nmipmap=1):
    
    peak_model = make_peak_model(settings)
    local_baseline_model = lmfit_models.LinearModel()
    biased_peak_model = peak_model + local_baseline_model
    
    nslices = data_ranges.nslices(*step_and_span(settings), nmipmap=nmipmap)
    slices  = data_ranges.slices(*step_and_span(settings), nmipmap=nmipmap)
    
    peaklist = []    
    #est_max_height = 1e-30
    print('Searching for peaks...')
    for i, d in enumerate(slices):
        
        if settings.flag_verbose:                        
            print("%3.1f%%" % (float(i) / float(nslices) * 100.0), end='\r')
            sys.stdout.flush()
        
        if len(d) == 0 or len(d[:, 0]) == 0:
            continue
        
        offset = d[0, 0]
        xxx = d[:, 0] - offset
        yyy = d[:, 1]
        
        # initital peak guess             
        params = peak_model.guess(yyy, x=xxx)
        params.add('slope', value=0.0)
        params.add('intercept', value=np.mean(yyy))

        # peak fitting loop
        scipy_leastsq_sett = {
            'maxfev': fev_per_epoch,
            'ftol':   1e-5,
            'xtol':   1e-5,
        }

        for n in range(0, nepochs):
            try:
                fit_out = biased_peak_model.fit(yyy, params, x = xxx,
                                                fit_kws = scipy_leastsq_sett)
            except:
                fit_out = None
                break
                
            params = fit_out.params
            fit_out.xxx = xxx 
            fit_out.yyy = yyy
            fit_out.offset = offset
            
            if converged_peak(fit_out): 
                break
            if not accept_peak(fit_out, settings):
                break
        
        if fit_out is None:
            continue
            
        # result of peak guess and fit
        if accept_peak(fit_out, settings):
            peaklist.append(fit_out)
            #if fit_out.params['height'] > est_max_height:
            #    est_max_height = fit_out.params['height']
    
    return peaklist
        

def peak_fwhm(peak):
    
    return peak.params['fwhm']

def peak_value(peak, flag_area = False):
    
    if not flag_area:
        return peak.params['height']
    else:
        full_area = np.trapz(peak.best_fit, x=peak.xxx)
        base_area = np.trapz(eval_local_baseline(peak), x=peak.xxx)
        
        return full_area - base_area

def peak_maximum(peak):
    
    return peak.params['center'] + peak.offset

def extract_peaks(peaklist, xxx, flag_area = False):
    
    calc_x    = np.linspace(xxx[0], xxx[-1], num = 2 * len(xxx))
    calc_y    = np.zeros(calc_x.shape)
    calc_ny_t = np.zeros(calc_x.shape)
    calc_ny   = np.zeros(calc_x.shape)
    
    for p in peaklist:
        index = bisect.bisect_left(calc_x, peak_maximum(p))
        
        if index <= 0 or index >= len(calc_x) - 1:
            continue
        
        calc_ny_t[index] += 1
        ny_i = calc_ny[index] + 1
        y_i  = calc_y[index] + peak_value(p, flag_area)
        
        if( calc_ny_t[index] >= calc_ny_t[index+1] 
            and calc_ny_t[index] >= calc_ny_t[index-1] ):
            di = 0
        elif( calc_ny_t[index+1] >= calc_ny_t[index] 
            and calc_ny_t[index+1] >= calc_ny_t[index-1] ):
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


def test_emission():
    """test example for emission spectra"""
    
    units = Units.spec_units()
    
    class LineProfileSettings: pass
    settings = LineProfileSettings() 
    settings.data_units       = units.GHz
    settings.min_fwhm         = 80  * units.kHz
    settings.max_fwhm         = 1.5 * units.MHz
    settings.step             = 1.0 * units.MHz 
    settings.nsigma           = 10
    settings.peak_model       = "Voigt"
    settings.flag_verbose     = True
    
    folder = "/home/borisov/InSync/astro_cologne/work/emission/advanced/"
    filename = folder + 'RT_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)#[5000:6500, :]
    
    # artificial baseline
    data[:, 1] += 0.1* np.sin(data[:, 0]*3)
    
    data_ranges = Ranges(arrays=[data])
    
    peaklist = find_peaks(data_ranges, settings)
    
    xxx = data[:, 0]
    obs = data[:, 1]
    calc_x, calc_y = extract_peaks(peaklist, xxx, flag_area = True)
        
    f1 = plt.figure(figsize=(11.69,8.27))
    ax1 = f1.add_subplot(211)
    ax2 = f1.add_subplot(212)
    
    ax1.set_xlabel(r"Frequency [GHz]")
    ax1.set_ylabel(r"Intensity [arb]")
    ax2.set_xlabel(r"Frequency [GHz]")
    ax2.set_ylabel(r"Peak area [arb * GHz]")
    ax1.ticklabel_format(axis='x', useOffset=False)
    ax2.ticklabel_format(axis='x', useOffset=False)
    
    ax1.plot(xxx, obs,  color = 'k', lw=1)
    ax2.plot(calc_x, calc_y * 1000, color = 'b', lw=1)
    for p in peaklist: 
        ax1.plot(p.xxx + p.offset, p.best_fit, color = 'r', lw=2)

    #plt.savefig(folder+'test.png', papertype = 'a4', orientation = 'landscape')
    plt.show()
    plt.close()
    
    # export calc spectrum
    np.savetxt(folder + "calc_area.txt", np.stack([calc_x, calc_y * 1000]).T)


def test_absorption():
    """test example for absortion spectra"""
    
    class LineProfileSettings: pass
    settings = LineProfileSettings() 
    settings.data_units       = units.MHz
    settings.min_fwhm         = 80  * units.kHz
    settings.max_fwhm         = 350  * units.kHz
    settings.avg_fwhm         = 200  * units.kHz
    settings.nsigma           = 10.0
    settings.peak_model       = "GaussDerivative"
    settings.flag_verbose     = True
    
    folder = "/home/borisov/InSync/astro_cologne/work/VinylCyanide/"
    
    arrays = []
    #for i in range(1, 11):
    #    filename = folder + 'dots_%i.dat' % i
    #    arrays += [np.loadtxt(filename)]
    
    arrays += [np.loadtxt(folder + 'survey.txt')]
    data_ranges = Ranges(arrays=arrays)
    data = data_ranges.export()
    
    peaklist = find_peaks(data_ranges, settings)
    
    xxx = data[:, 0]
    obs = data[:, 1]
    calc_x, calc_y = extract_peaks(peaklist, xxx, flag_area = False)
        
    f1 = plt.figure(figsize=(11.69,8.27))
    ax1 = f1.add_subplot(211)
    ax2 = f1.add_subplot(212)
    
    ax1.set_xlabel(r"Frequency [MHz]")
    ax1.set_ylabel(r"Intensity [arb]")
    ax2.set_xlabel(r"Frequency [MHz]")
    ax2.set_ylabel(r"Peak area [arb * MHz]")
    ax1.ticklabel_format(axis='x', useOffset=False)
    ax2.ticklabel_format(axis='x', useOffset=False)
    
    ax1.plot(xxx, obs,  color = 'k', lw=1)
    ax2.plot(calc_x, calc_y * 1000, color = 'b', lw=1)
    for p in peaklist: 
        ax1.plot(p.xxx + p.offset, p.best_fit, color = 'r', lw=2)
        ax1.plot(p.xxx + p.offset, eval_local_baseline(p), color = 'g', lw=1)

    #plt.savefig(folder+'test.png', papertype = 'a4', orientation = 'landscape')
    plt.show()
    plt.close()
    
    # export calc spectrum
    #np.savetxt(folder + "calc.txt", np.stack([calc_x, calc_y * 1000]).T)
    with open(folder + "survey_peaks_raw.txt", 'w') as f:
        for p in peaklist:
            freq = (peak_maximum(p) * settings.data_units).to(units.MHz).magnitude
            intens = np.log10( peak_value(p, flag_area=True) )
            error = (peak_fwhm(p) * settings.data_units).to(units.MHz).magnitude
            f.write("{}\t{}\t{}\n".format(freq, error, intens))
            
    
if __name__ == '__main__':
    test_absorption()
    #test_emission()
