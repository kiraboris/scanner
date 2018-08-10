
import os.path

from gui.pyqtgraph.Qt import QtCore
from . import simulation_object
from . import unique_name_holder


class SimulationGroup(QtCore.QObject, unique_name_holder.UniqueNameHolder):
    def __init__(self, ranges, parent=None):
        QtCore.QObject.__init__(self, parent)
        unique_name_holder.UniqueNameHolder.__init__(self)
        self.ranges = ranges
        self.__objects = []
        self.defaults = simulation_object.SimulationParams()

    def add_rotor(self, filename):
        basepath, extension = os.path.splitext(filename)
        if not self._check_name(basepath):
            return

        try:
            rotor = simulation_object.SimulationObject(basepath, extension)
        except:
            return

        self.__objects.append(rotor)
        self.update_range(len(self.__rotors)-1)

    def update_range(self, index):
        self.ranges.update(index, self.__objects[index].make_spectrum())

