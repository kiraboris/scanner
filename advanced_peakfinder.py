
import matplotlib.pyplot as plt
import numpy as np
import bisect

import lmfit.models as lmfit_models 
import lmfit.model lmfit_model_base

import basetypes
from basetypes import DIM 

class PVoigtDerivedModel(lmfit_model_base.Model):
    fwhm_factor = 2*np.sqrt(2*np.log(2))
    height_factor = 1./np.sqrt(2*np.pi)
    
    def __init__(self, independent_vars=['x'], prefix='', nan_policy='raise',
                 derivative_order = 0, **kwargs):
        kwargs.update({'prefix': prefix, 'nan_policy': nan_policy,
                       'independent_vars': independent_vars})

        if derivative_order == 0:
            self.function = self.pvoigt
            self.
        elif derivative_order == 1:
        
        super(PVoigtDerivedModel, self).__init__(self.function, **kwargs)
        self._set_paramhints_prefix()

    def _set_paramhints_prefix(self):
        self.set_param_hint('sigma', min=0)
        self.set_param_hint('fraction', value=0.5, min=0.0, max=1.0)
        self.set_param_hint('fwhm', expr=fwhm_expr(self))
        fmt = ("(((1-{prefix:s}fraction)*{prefix:s}amplitude)/"
               "({prefix:s}sigma*sqrt(pi/log(2)))+"
               "({prefix:s}fraction*{prefix:s}amplitude)/"
               "(pi*{prefix:s}sigma))")
        self.set_param_hint('height', expr=fmt.format(prefix=self.prefix))

    def guess(self, data, x=None, negative=False, **kwargs):
        pars = guess_from_peak(self, data, x, negative, ampscale=1.25)
        pars['%sfraction' % self.prefix].set(value=0.5, min=0.0, max=1.0)
        return update_param_vals(pars, self.prefix, **kwargs)
        
    
    @staticmethod
    def pvoigt(x, amplitude=1.0, center=0.0, sigma=1.0, fraction=0.5):
        sigma_g = sigma / sqrt(2*log2)
        return ((1-fraction)*gaussian(x, amplitude, center, sigma_g) +
                fraction*lorentzian(x, amplitude, center, sigma))
            
    @staticmethod
    def pvoigt_prime(x, amplitude=1.0, center=0.0, sigma=1.0, fraction=0.5):
        sigma_g = sigma / sqrt(2*log2)
        return ((1-fraction)*gaussian(x, amplitude, center, sigma_g) +
                fraction*lorentzian(x, amplitude, center, sigma))



def step_and_span(settings):
    
    step = 1.0 * settings.max_fwhm.to(settings.data_units).magnitude 
        
    span = 4.0 * settings.max_fwhm.to(settings.data_units).magnitude
    
    return step, span
    
def accept_peak(peak, settings, xxx, yyy):
    """fidelity test for peak candidates"""
    
    flag1 = (abs(peak.params['height']) >= settings.min_height)

    flag2 = (peak.params['fwhm'] >=
        settings.min_fwhm.to(settings.data_units).magnitude)
        
    flag3 = (peak.params['fwhm'] <=
        settings.max_fwhm.to(settings.data_units).magnitude)
        
    # candidate has a maximum
    flag4 = (xxx[0] < peak.params['center'] < xxx[-1])
    
    # slope not extreme
    max_slope_estimate = (np.max(yyy) - np.min(yyy)) / (xxx[-1] - xxx[0])
    flag5 = (abs(peak.params['slope']) <= max_slope_estimate)
        
    return flag1 and flag2 and flag3 and flag4 and flag5

def converged_peak(peak):
    return peak.ier in range(1, 5)  
    # see https://docs.scipy.org/doc/scipy/reference/
    #    generated/scipy.optimize.leastsq.html 


def find_peaks(data_ranges, settings, fev_per_epoch = 16, nepochs = 4):
    
    peak_model = lmfit_models.PseudoVoigtModel()     # TODO: derivatives
    local_baseline_model = lmfit_models.LinearModel()
    biased_peak_model = peak_model + local_baseline_model
    
    nslices = data_ranges.nslices(*step_and_span(settings), nmipmap=2)
    slices  = data_ranges.slices(*step_and_span(settings), nmipmap=2)

    peaklist = []    
    print('Searching for peaks...')
    for i, d in enumerate(slices):
        offset = d[0, 0]
        xxx = d[:, 0] - offset
        yyy = d[:, 1]
        
        # initital peak guess             
        params = peak_model.guess(yyy, x=xxx)
        params.add('intercept', value=np.mean(yyy))
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
            params = fit_out.params
            if converged_peak(fit_out): 
                break
            if not accept_peak(fit_out, settings, xxx, yyy):
                break

        # result of peak guess and fit
        if accept_peak(fit_out, settings, xxx, yyy):
            fit_out.offset = offset
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
        xxx = peak.xxx
        full_area = np.trapz(peak.best_fit, x=xxx)
        
        # revive local baseline model from fitted peak to subtract baseline area
        local_baseline_model = lmfit_models.LinearModel()
        params = local_baseline_model.make_params()
        params['intercept'].set(value = peak.params['intercept']) 
        params['slope'].set(value = peak.params['slope'])
        
        xxx = peak.xxx - peak.offset
        base_area = np.trapz(local_baseline_model.eval(params, x=xxx), x=xxx)
        
        return full_area - base_area

def extract_peaks(peaklist, xxx, flag_area = False):
    
    calc_x    = np.linspace(xxx[0], xxx[-1], num = 2 * len(xxx))
    calc_y    = np.zeros(calc_x.shape)
    calc_ny_t = np.zeros(calc_x.shape)
    calc_ny   = np.zeros(calc_x.shape)
    
    for p in peaklist:
        index = bisect.bisect_left(calc_x, p.params['center'])
        
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
    settings.min_height       = 0.001
    settings.derivative_order = 0
    
    folder = "/home/borisov/projects/work/emission/advanced/"
    filename = folder + 'RT_norm_mean_spec.txt'
    
    data = np.loadtxt(filename)[4000:6500, :]
    
    # artificial baseline
    data[:, 1] += 0.1* np.sin(data[:, 0]*3)
    
    data_ranges = basetypes.Ranges(arrays=[data])
    
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
    ax2.set_ylabel(r"Peak area [arb * MHz]")
    ax1.ticklabel_format(axis='x', useOffset=False)
    ax2.ticklabel_format(axis='x', useOffset=False)
    
    ax1.plot(xxx, obs,  color = 'k', lw=1)
    ax2.plot(calc_x, calc_y * 1000, color = 'b', lw=1)
    for p in peaklist: 
        ax1.plot(p.xxx, p.best_fit, color = 'r', lw=2)

    #plt.savefig(folder+'test.png', papertype = 'a4', orientation = 'landscape')
    plt.show()
    plt.close()
    
    # export calc spectrum
    np.savetxt(folder + "calc_area.txt", np.stack([calc_x, calc_y * 1000]).T)


def test_absorption():
    """test example for absortion spectra"""
    
    units = basetypes.Units.spec_units()
    
    class LineProfileSettings: pass
    settings = LineProfileSettings() 
    settings.data_units       = units.MHz
    settings.min_fwhm         = 50  * units.kHz
    settings.max_fwhm         = 500 * units.kHz
    settings.min_height       = 10.0
    settings.derivative_order = 1
    
    folder = "/home/borisov/projects/work/emission/advanced/"
    filename = folder + 'expdata_38-44.dat'
    
    data = np.loadtxt(filename)[5500:6500, :]
    data_ranges = Ranges(arrays=[data])
    
    peaklist = find_peaks(data_ranges, settings)
    
    xxx = data[:, 0]
    obs = data[:, 1]
    #calc_x, calc_y = extract_peaks(peaklist, xxx, flag_area = True)
        
    f1 = plt.figure(figsize=(11.69,8.27))
    ax1 = f1.add_subplot(211)
    ax2 = f1.add_subplot(212)
    
    ax1.set_xlabel(r"Frequency [GHz]")
    ax1.set_ylabel(r"Intensity [arb]")
    ax2.set_xlabel(r"Frequency [GHz]")
    ax2.set_ylabel(r"Peak area [arb * MHz]")
    ax1.ticklabel_format(axis='x', useOffset=False)
    ax2.ticklabel_format(axis='x', useOffset=False)
    
    ax1.plot(xxx, obs,  color = 'k', lw=1)
    #ax2.plot(calc_x, calc_y * 1000, color = 'b', lw=1)
    for p in peaklist: 
        ax1.plot(p.xxx, p.best_fit, color = 'r', lw=2)

    #plt.savefig(folder+'test.png', papertype = 'a4', orientation = 'landscape')
    plt.show()
    plt.close()
    
    # export calc spectrum
    #np.savetxt(folder + "calc_area.txt", np.stack([calc_x, calc_y * 1000]).T)
    
if __name__ == '__main__':
    test_emission()
