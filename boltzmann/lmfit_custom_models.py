
import numpy as np
import lmfit.models as lmfit_models 
import lmfit.model as lmfit_model_base

class GaussDerivativeModel(lmfit_model_base.Model):

    height_fmt = "-0.5*sqrt(2)*{prefix:s}amplitude/(sqrt(pi)*{prefix:s}sigma**3)"
    fwhm_factor = 0.625937683618476
    
    @staticmethod
    def gaussian_second_derivative(x, amplitude=1.0, center=0.0, sigma=1.0):
        return (0.5*np.sqrt(2)*amplitude*(-1 + (center - x)**2/sigma**2)*
            np.exp(-(center - 1.0*x)**2/(2*sigma**2))/(np.sqrt(np.pi)*sigma**3))
        # this expression as well as above were generated with SymPy
    
    
    def __init__(self, independent_vars=['x'], prefix='', nan_policy='raise',
                 **kwargs):
        kwargs.update({'prefix': prefix, 'nan_policy': nan_policy,
                       'independent_vars': independent_vars})
        super(GaussDerivativeModel, self).__init__(self.gaussian_second_derivative,
                                                   **kwargs)
        self._set_paramhints_prefix()

    def _set_paramhints_prefix(self):
        self.set_param_hint('sigma', min=0)
        self.set_param_hint('fwhm', expr=lmfit_models.fwhm_expr(self))
        self.set_param_hint('height', expr=self.height_fmt.format(prefix=self.prefix))
    
    def guess(self, data, x=None, negative=False, **kwargs):
        pars = lmfit_models.guess_from_peak(self, data, x, negative)
        return lmfit_models.update_param_vals(pars, self.prefix, **kwargs)
    
    __init__.__doc__ = lmfit_models.COMMON_INIT_DOC
    guess.__doc__ = lmfit_models.COMMON_GUESS_DOC
