from collections import namedtuple
import numpy as np
import sys

import pint
import lmfit
import lmfit.models as lmfit_models

from basetypes import StructFactory, Ranges


class LineProfileSettings(StructFactory.make(
    'gaussian_fwhm_estimate',
    'lorentzian_fwhm_estimate',
    'derivative_order'
    'data_units'
    )): pass


def voigt_param_estimate(settings):
    
    fL = settings.lorentzian_fwhm_estimate.to(settings.data_units).magnitude
    fG = settings.gaussian_fwhm_estimate.to(settings.data_units).magnitude
    
    fwhm = 0.5*fL + (0.2*fL**2 + fG**2)**0.5
    frac = fL / (fG + fL)
    
    return {'fwhm': fwhm, 'fraction': frac}
    

def step_and_span(settings, step_nw =1.0, span_nw = 3.0):
    
    estimate = voigt_param_estimate(settings)
    
    step = step_nw * estimate['fwhm']
    span = span_nw * estimate['fwhm']
    
    return step, span
    

def find_peaks(data, settings):
    
    data_ranges = Ranges(arrays=[data])
    
    # TODO: take account of derivatives
    peak_model = lmfit_models.PseudoVoigtModel()
    base_model = lmfit_models.LinearModel()
    model = peak_model + base_model
    
    estimate = voigt_param_estimate(settings)
    params = model.make_params() 
    params['fwhm'].set(value=estimate['fwhm'], 
        min=0.2*estimate['fwhm'], max=5*estimate['fwhm'])
    params['fraction'].set(value=estimate['fraction'], 
        min=0.0, max=1.0)
    
    peaklist = []
    print('Searching for peaks...')
    nslices = data_ranges.nslices(*step_and_span(settings), dim=0)
    slices  = data_ranges.slices(*step_and_span(settings), dim=0)
    
    for i, d in enumerate(slices):
        xxx = d[:, 0]
        yyy = d[:, 1]
        
        params['center'].set(value=((xxx[0] + xxx[-1]) / 2),
            min=xxx[0], max=xxx[-1])
        params['amplitude'].set(value=np.mean(yyy), 
            min=0.0, max=np.max(yyy)-np.min(yyy))
                            
        fit_out = model.fit(yyy, params, 
                            x=xxx, fit_kws={'maxfev': 15})
                            
        print("%i%%" % int(i / float(nslices) * 100), end='\r')
        sys.stdout.flush()
        peaklist.append(fit_out)
        
    return peaklist
        

def test():
    # test example for emission spectra
    
    units = pint.UnitRegistry('units.txt')
    
    settings = LineProfileSettings() 
    
    settings.data_units = units.GHz
    settings.gaussian_fwhm_estimate   = 400 * units.kHz
    settings.lorentzian_fwhm_estimate = 200 * units.kHz
    settings.derivative_order = 0
    
    folder = "/home/borisov/projects/work/emission/simple_model/"
    filename = folder + 'RT_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)
    
    peaklist = find_peaks(data, settings)
    
    peaklist_sorted = sorted(peaklist, 
        key=lambda p: float(p.params['amplitude']), reverse=True)

    print('')        
    print('30 most instense peaks:')   
    for p in peaklist_sorted[:30]:    
        print(float(p.params['amplitude']))
        
    
    
if __name__ == '__main__':
    test()
