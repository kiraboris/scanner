
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
        self.defaults = defaults
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

    def update_lines(self, **kwargs):
        params = copy.copy(self.defaults)
        params.set(kwargs)
        self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                       threshold=params.threshold,
                                                       max_freq=params.max_freq)

    def make_spectrum(self, **kwargs):
        params = copy.copy(self.defaults)
        params.set(kwargs)
        return spectrum_tools.make_rotor_spectrum(self.rotor, params)

    def make_info(self):
        info = {}
        info['Method'] = self.qworker.name()
        #info['X Resolution'] = str(self.params.resolution) + ' ' + str(self.params.x_unit_name)
        #info['X Min'] = str(self.params.min_freq) + ' ' + str(self.params.x_unit_name)
        #info['X Max'] = str(self.params.max_freq) + ' ' + str(self.params.x_unit_name)
        info['Y Threshold'] = str(self.defaults.threshold) + " PU"
        info['Y Factor'] = str(self.defaults.intensity_factor)
        info['u_A'] = str(self.rotor.mu_A) + " D"
        info['u_B'] = str(self.rotor.mu_B) + " D"
        info['u_C'] = str(self.rotor.mu_C) + " D"
        return info

    def set_params(self, info):
        # try:
        #     self.params.resolution = float(info['X Resolution'].strip().split()[0])
        # except:
        #     pass
        # try:
        #     self.params.min_freq = float(info['X Min'].strip().split()[0])
        # except:
        #     pass
        # try:
        #     self.params.max_freq = float(info['X Max'].strip().split()[0])
        # except:
        #     pass
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