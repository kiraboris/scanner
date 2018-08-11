
from entities.rotor import Rotor

import pickett
from . import spectrum_tools


class SimulationParams:
    def __init__(self, resolution=None, min_freq=None, max_freq=None, threshold=None, intensity_factor=None):
        self.intensity_factor = intensity_factor
        self.resolution = resolution
        self.threshold = threshold   # minumum intensity in Pickett units
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.x_unit_name = 'MHz'


class SimulationObject:
    def __init__(self, basepath, extension, params):
        self.rotor = Rotor()
        self.basepath = basepath
        self.params = params
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

    def update_lines(self):
        self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                       threshold=self.params.threshold,
                                                       max_freq=self.params.max_freq)

    def make_spectrum(self, min_freq=None, max_freq=None):
        if not min_freq:
            min_freq = self.params.min_freq
        if not max_freq:
            max_freq = self.params.max_freq
        return spectrum_tools.make_rotor_spectrum(self.rotor, min_freq, max_freq, self.params)

    def make_info(self):
        info = {}
        info['Method'] = self.qworker.name()
        #info['X Resolution'] = str(self.params.resolution) + ' ' + str(self.params.x_unit_name)
        #info['X Min'] = str(self.params.min_freq) + ' ' + str(self.params.x_unit_name)
        #info['X Max'] = str(self.params.max_freq) + ' ' + str(self.params.x_unit_name)
        info['Y Threshold'] = str(self.params.threshold) + " PU"
        info['Y Factor'] = str(self.params.intensity_factor)
        info['u_A'] = str(self.rotor.mu_A) + " D"
        info['u_B'] = str(self.rotor.mu_B) + " D"
        info['u_C'] = str(self.rotor.mu_C) + " D"
        return info