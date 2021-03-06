
import copy

from entities.rotor import Rotor

import pickett
from . import spectrum_tools
from . import simulation_params


class SimulationObject:
    def __init__(self, basepath, extension, defaults):
        self.rotor = Rotor()
        self.basepath = basepath
        self.__defaults = copy.copy(defaults)
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
            params = self.__defaults
        return not self._are_current_params_sufficient(params)

    def _are_current_params_sufficient(self, params):
        if not self.__current_params:
            return False
        elif self.__current_params.threshold > params.threshold:
            return False
        elif self.__current_params.max_freq < params.max_freq:
            return False
        elif self.__current_params.J_min > params.J_min:
            return False
        elif self.__current_params.J_max < params.J_max:
            return False
        else:
            return True

    def update_lines(self, params=None):
        if params is None:
            params = copy.copy(self.__defaults)
            params.threshold = self.__defaults.threshold
            params.max_freq = self.__defaults.max_freq * 1.5
            params.J_max = int(self.__defaults.J_max * 1.5)
            params.J_min = 0
        self.rotor.sim_lines = self.qworker.make_lines(self.rotor,
                                                       inten=params.threshold,
                                                       max_freq=params.max_freq / 1000,
                                                       J_min=params.J_min,
                                                       J_max=params.J_max)
        self.__current_params = copy.copy(params)
        self.rotor.flag_changed = False

    def make_spectrum(self, params=None):
        if self.need_update_lines(params):
            self.update_lines(params)
        if not params:
            spec = spectrum_tools.make_rotor_spectrum(self.rotor, self.__defaults)
        else:
            spec = spectrum_tools.make_rotor_spectrum(self.rotor, params)
        return spec

    def make_sim_settings_info(self):
        return self.__defaults.make_ui_dict(self.rotor)

    def make_rotor_params_info(self):
        names = []
        checked = {}
        infos = {}
        for i, (name, param) in enumerate(self.rotor.params.items()):
            info = ("%.6e" % param.value)
                    #' (' + ("%.4f" % (100.0 - param.error / param.value * 100)).rstrip('0').rstrip('.') + "%)")
            names.append(name)
            checked[i] = param.flag_fit
            infos[i] = info
        max_len = max([len(name) for name in names])
        for i, name in enumerate(names):
            cur_len = len(name)
            spaces = " " * int((max_len - cur_len) + 4 + (0 if infos[i][0] == '-' else 1))
            names[i] = name + spaces + infos[i]
        return names, checked

    def set_defaults(self, obj):
        if isinstance(obj, simulation_params.SimulationParams):
            self.__defaults = copy.copy(obj)
        else:
            self.__defaults.set_from_ui_dict(obj)
