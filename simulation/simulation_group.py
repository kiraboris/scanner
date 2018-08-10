
import os.path

from gui.pyqtgraph.Qt import QtCore
from . import simulation_object
from . import unique_name_holder


class SimulationGroup(QtCore.QObject, unique_name_holder.UniqueNameHolder):

    sigUpdateRange = QtCore.Signal(int, object)

    def __init__(self, ranges, parent=None):
        QtCore.QObject.__init__(self, parent)
        unique_name_holder.UniqueNameHolder.__init__(self)
        self.__objects = []
        self.__defaults = simulation_object.SimulationParams()

    def add_rotor(self, filename):
        basepath, extension = os.path.splitext(filename)
        if not self._check_name(basepath):
            return

        try:
            rotor = simulation_object.SimulationObject(basepath, extension, self.__defaults)
        except:
            return

        index = len(self.__rotors)-1
        self._add_unique_names({index: basepath})
        self.__objects.append(rotor)
        self._emit_update_range(index)

    #def make_spectrum(self, index):

    def _emit_update_range(self, index):
        self.sigUpdateRange.emit(index, self.__objects[index].make_spectrum())

    def set_defaults(self, **kwargs):
        self.__defaults = simulation_object.SimulationParams(**kwargs)

