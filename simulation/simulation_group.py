
import os.path

from gui.pyqtgraph.Qt import QtCore
from . import simulation_object
from . import unique_name_holder


class SimulationGroup(QtCore.QObject, unique_name_holder.UniqueNameHolder):

    sigUpdateRange = QtCore.Signal(int, object)
    sigAdded = QtCore.Signal(str)

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
                #self._make_spectrum(index, flag_update_lines=True)
                self.sigAdded.emit(obj.rotor.name)
            except:
                return

    def _make_spectrum(self, index, flag_update_lines=False):
        if flag_update_lines:
            self.__objects[index].update_lines()
        spec = self.__objects[index].make_spectrum()
        self.sigUpdateRange.emit(index, spec)

    def set_defaults(self, **kwargs):
        self.__defaults = simulation_object.SimulationParams(**kwargs)

