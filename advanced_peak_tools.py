from collections import namedtuple
import numpy as np

import lmfit
import lmfit.models as lmfit_models

from basetypes import StructFactory, Ranges


class LineProfileSettings(StructFactory.make(
    'gaussian_fwhm_estimate',
    'lorentzian_fwhm_estimate',
    'derivative_order'
    ): pass


def voigt_param_estimate(line_profile_settings):
    
    fL = line_profile_settings.lorentzian_fwhm_estimate
    fG = line_profile_settings.gaussian_fwhm_estimate
    
    fwhm = 0.5*fL + (0.2*fL**2 + fG**2)**0.5
    frac = fL / (fG + fL)
    
    return namedtuple("tup_vpe", "fwhm", "frac")(fwhm=fwhm, frac=frac)
    

def make_slices(data_ranges, line_profile_settings, step_nw = 1, span_nw = 3):
    
    estimate = voigt_fwhm_estimate(line_profile_settings)
    
    step = step_nw * estimate.fwhm
    span = span_nw * estimate.fwhm
    
    return data_ranges.slices(step, span, dim=0)
    

def find_peaks(data, line_profile_settings):
    
    data_ranges = Ranges(arrays=[data])
    
    # TODO: take account of derivatives
    peak_model = lmfit_models.PseudoVoigtModel()
    base_model = lmfit_models.LinearModel()
    model = peak_model + base_model
    
    estimate = voigt_fwhm_estimate(line_profile_settings)
    
    params_guess = model.make_params(amplitude=1.0, 
                                     fwhm=estimate.fwhm, fraction=estimate.frac) 
    
    peaklist = []
    for data_slice in make_slices(data_ranges, line_profile_settings):
        xxx = data_slice[:, 0]
        yyy = data_slice[:, 1]
        fit_out = model.fit(yyy, params_guess, x=xxx)
        peaklist.append(fit_out)
        
    return peaklist
        

def test():
    # test example for emission spectra
    
    settings = LineProfileSettings() 

    settings.gaussian_fwhm_estimate   = 100  # kHz
    settings.lorentzian_fwhm_estimate = 10   # kHz
    settings.derivative_order = 0
    
    folder = "./"
    filename = folder + suffix + '340K_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)
    
    peaklist = find_peaks(data, settings)
    
    
if __name__ == '__main__':
    test()
