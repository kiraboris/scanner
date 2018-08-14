
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
        if self.rotor.flag_changed:
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
            self.rotor.flag_changed = False
        else:
            self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                           threshold=params.threshold,
                                                           max_freq=params.max_freq / 1000)
            self.__current_params = copy.copy(params)
            self.rotor.flag_changed = False

    def make_spectrum(self, params=None):
        if self.need_update_lines(params):
            self.update_lines(params)

        if not params:
            spec = spectrum_tools.make_rotor_spectrum(self.rotor, self.defaults)
        else:
            spec = spectrum_tools.make_rotor_spectrum(self.rotor, params)

        return spec

    def make_info(self):
        info = {}
        info['Y Threshold'] = str(self.defaults.threshold) + " PU"
        info['Y Factor'] = str(self.defaults.intensity_factor)
        info['Sigma'] = str(self.defaults.sigma) + " " + str(self.defaults.x_unit_name)
        return info

    def make_rotor_params_info(self):
        names = []
        checked = {}
        for i, (name, param) in enumerate(self.rotor.params.items()):
            text = name + " = %.6e" % (param.value)
            names.append(text)
            checked[i] = param.flag_fit

        return names, checked

    def set_params(self, info):
        if isinstance(info, SimulationParams):
            self.defaults = copy.copy(info)
        else:  # dict from ui
            try:
                self.defaults.intensity_factor = float(info['Y Factor'].strip().split()[0])
            except:
                pass
            try:
                self.defaults.threshold = float(info['Y Threshold'].strip().split()[0])
            except:
                pass
            try:
                self.defaults.sigma = float(info['Sigma'].strip().split()[0])
            except:
                pass