
#import copy
import os.path

from gui.pyqtgraph.Qt import QtCore
from . import simulation_object
from . import unique_name_holder


class SimulationGroup(QtCore.QObject, unique_name_holder.UniqueNameHolder):

    sigUpdateRange = QtCore.Signal(int, object)
    sigRemoveRange = QtCore.Signal(int)
    sigLockRanges = QtCore.Signal(bool)
    sigAdded = QtCore.Signal(str)
    sigInfo = QtCore.Signal(dict)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        unique_name_holder.UniqueNameHolder.__init__(self)
        self.__objects = []
        self.__defaults = simulation_object.SimulationParams()

    def add_rotor(self, filename):
        basepath, extension = os.path.splitext(filename)
        if self._check_name(basepath):
            try:
                obj = simulation_object.SimulationObject(basepath, extension, self.__defaults)
                index = len(self.__objects)
                self._add_unique_names({index: basepath})
                self.__objects.append(obj)
                self._emit_spectrum(index)
                self.sigAdded.emit(obj.rotor.name)
            except:
                return

    def remove_rotor(self, index):
        if index < len(self.__objects):
            del self.__objects[index]
            self._remove_unique_name(index)
            self.sigRemoveRange.emit(index)

    def _emit_spectrum(self, index):
        spec = self.__objects[index].make_spectrum()
        self.sigUpdateRange.emit(index, spec)

    def _emit_all_spectra(self):
        self.sigLockRanges.emit(True)
        for index in range(0, len(self.__objects)):
            self._emit_spectrum(index)
        self.sigLockRanges.emit(False)

    def set_defaults(self, flag_override=False, **kwargs):
        self.__defaults.set(**kwargs)
        if flag_override:
            for obj in self.__objects:
                obj.set_params(self.__defaults)
            self._emit_all_spectra()

    def set_boundaries(self, xmin, xmax):
        self.set_defaults(flag_override=True, min_freq=xmin, max_freq=xmax)

    def get_settings(self, index):
        info_dict = self.__objects[index].make_info()
        self.sigInfo.emit(info_dict)

    def apply_settings(self, index, new_info):
        old_info = self.__objects[index].make_info()
        if new_info != old_info:
            self.__objects[index].set_params(new_info)
            self._emit_spectrum(index)
        self.get_settings(index)
