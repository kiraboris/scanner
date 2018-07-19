import numpy as np
import sys

import lmfit.models as lmfit_models
from boltzmann import lmfit_custom_models


def step_and_span(settings):
    
    step = settings.step.to(settings.data_units).magnitude
        
    span = 3 * step
    
    return step, span
    
    
def accept_peak(peak, settings, biased_peak_model):
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
    
    if not flag1 or not flag2 or not flag3:
        return False
    
    # line height positive and greater than noise height
    yyy_noise = yyy - biased_peak_model.eval(peak.params, x=peak.xxx)
    min_height_estimate = settings.nsigma * np.std(yyy_noise)    
    flag4 = (peak.params['height'] >= min_height_estimate)
    
    if not flag4:
        return False
    
    return True


def converged_peak(peak):
    return peak.ier in range(1, 5)  
    # see https://docs.scipy.org/doc/scipy/reference/
    #    generated/scipy.optimize.leastsq.html 


def eval_local_baseline(peak):
    
    local_baseline_model = lmfit_models.QuadraticModel()
    params = local_baseline_model.make_params()
    params['a'].set(value = peak.params['a']) 
    params['b'].set(value = peak.params['b'])   
    params['c'].set(value = peak.params['c'])   

    return local_baseline_model.eval(params, x=peak.xxx)


def make_peak_model(settings):
    
    if settings.peak_model == "GaussDerivative":
        return lmfit_custom_models.GaussDerivativeModel()
    elif settings.peak_model == "Voigt": 
        return lmfit_models.PseudoVoigtModel()
    else:
        return lmfit_models.GaussianModel()

def find_peaks(data_ranges, settings, 
               fev_per_epoch = 16, nepochs = 4, nmipmap = 1):
    
    peak_model = make_peak_model(settings)
    local_baseline_model = lmfit_models.QuadraticModel()
    biased_peak_model = peak_model + local_baseline_model
    
    nslices = data_ranges.nslices(*step_and_span(settings), nmipmap=nmipmap)
    slices  = data_ranges.slices(*step_and_span(settings), nmipmap=nmipmap)
    
    peaklist = []    
    #est_max_height = 1e-30
    print('Searching for peaks...')
    for i, d in enumerate(slices):
        
        if len(d) == 0 or len(d[:, 0]) == 0:
            continue
        
        offset = d[0, 0]
        xxx = d[:, 0] - offset
        yyy = d[:, 1]
        
        # initital peak guess             
        params = peak_model.guess(yyy, x=xxx)
        params.add('a', value=0.0)
        params.add('b', value=0.0)
        params.add('c', value=np.mean(yyy))

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
            if not accept_peak(fit_out, settings, biased_peak_model):
                break
        
        if fit_out is None:
            continue
            
        # result of peak guess and fit
        if accept_peak(fit_out, settings, biased_peak_model):
            peaklist.append(fit_out)
            #if fit_out.params['height'] > est_max_height:
            #    est_max_height = fit_out.params['height']
        
        if settings.flag_verbose:                        
            print("%3.1f%%" % (float(i) / float(nslices) * 100.0), end='\r')
            sys.stdout.flush()
    
    return peaklist
        

def peak_value(peak, flag_area = False):
    
    if not flag_area:
        return peak.params['height']
    else:
        full_area = np.trapz(peak.best_fit, x=peak.xxx)
        base_area = np.trapz(eval_local_baseline(peak), x=peak.xxx)
        
        return full_area - base_area

def peak_maximum(peak):
    
    return peak.params['center'] + peak.offset
