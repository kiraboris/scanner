
import copy

from entities.rotor import Rotor

import pickett
from . import spectrum_tools


class SimulationParams:
    def __init__(self, sigma=None, resolution=None, min_freq=None, max_freq=None, threshold=None, intensity_factor=None):
        self.intensity_factor = intensity_factor
        self.resolution = resolution
        self.threshold = threshold  # minumum intensity in Pickett units
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.x_unit_name = 'MHz'
        self.sigma = sigma

    def set(self, sigma=None, resolution=None, min_freq=None, max_freq=None, threshold=None, intensity_factor=None):
        if intensity_factor:
            self.intensity_factor = intensity_factor
        if resolution:
            self.resolution = resolution
        if threshold:
            self.threshold = threshold   # minumum intensity in Pickett units
        if min_freq:
            self.min_freq = min_freq
        if max_freq:
            self.max_freq = max_freq
        if sigma:
            self.sigma = sigma


class SimulationObject:
    def __init__(self, basepath, extension, defaults):
        self.rotor = Rotor()
        self.basepath = basepath
        self.defaults = copy.copy(defaults)
        self.__current_params = None
        self.load_rotor(basepath, extension)

    def __setup_qworker(self, extension):
        if extension in pickett.valid_extensions():
            self.qworker = pickett
        else:
            raise Exception()

    def load_rotor(self, basepath, extension):
        self.__setup_qworker(extension)
        try:
            self.qworker.load_rotor(self.rotor, self.basepath)
        except:
            raise Exception()

    def need_update_lines(self, params=None):
        if self.rotor.needs_update_lines():
            return True
        if not params:
            params = self.defaults
        return not self._are_current_params_sufficient(params)

    def _are_current_params_sufficient(self, params):
        if not self.__current_params:
            return False
        elif self.__current_params.threshold > params.threshold:
            return False
        elif self.__current_params.max_freq < params.max_freq:
            return False
        else:
            return True

    def update_lines(self, params=None):
        if params is None:
            max_freq = self.defaults.max_freq * 2
            self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                           threshold=self.defaults.threshold,
                                                           max_freq=max_freq / 1000)
            self.__current_params = copy.copy(self.defaults)
            self.__current_params.max_freq = max_freq
        else:
            self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                           threshold=params.threshold,
                                                           max_freq=params.max_freq / 1000)
            self.__current_params = copy.copy(params)

    def make_spectrum(self, params=None):
        if self.need_update_lines(params):
            self.update_lines(params)
        spec = spectrum_tools.make_rotor_spectrum(self.rotor, params)
        return spec

    def make_info(self):
        info = {}
        info['Method'] = self.qworker.name()
        info['Y Threshold'] = str(self.defaults.threshold) + " PU"
        info['Y Factor'] = str(self.defaults.intensity_factor)
        info['u_A'] = str(self.rotor.mu_A) + " D"
        info['u_B'] = str(self.rotor.mu_B) + " D"
        info['u_C'] = str(self.rotor.mu_C) + " D"
        return info

    def set_params(self, info):
        if isinstance(info, SimulationParams):
            self.defaults = copy.copy(info)
        else:
            try:
                self.defaults.intensity_factor = float(info['Y Factor'].strip().split()[0])
            except:
                pass
            try:
                self.defaults.threshold = float(info['Y Threshold'].strip().split()[0])
            except:
                pass
            try:
                self.rotor.mu_A = float(info['u_A'].strip().split()[0])
            except:
                pass
            try:
                self.rotor.mu_B = float(info['u_B'].strip().split()[0])
            except:
                pass
            try:
                self.rotor.mu_C = float(info['u_C'].strip().split()[0])
            except:
                pass