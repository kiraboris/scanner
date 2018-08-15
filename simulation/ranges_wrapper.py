
import os.path

from gui.pyqtgraph.Qt import QtCore
from entities import ranges
from . import unique_name_holder


class RangesWrapper(QtCore.QObject, ranges.Ranges, unique_name_holder.UniqueNameHolder):

    sigUpdated = QtCore.Signal(object)
    sigAdded = QtCore.Signal(list)
    sigInfo = QtCore.Signal(dict)
    sigBoundaries = QtCore.Signal(float, float, float)
    log = QtCore.Signal(str)

    def __init__(self, parent=None, **kwargs):
        QtCore.QObject.__init__(self, parent)
        ranges.Ranges.__init__(self, **kwargs)
        unique_name_holder.UniqueNameHolder.__init__(self)
        self.__x_unit_name = "MHz"
        self.__y_unit_name = "arb"
        self.__x_min = None
        self.__x_max = None
        self.__x_res = None
        self.__locked = False

    @staticmethod
    def __make_basenames(names):
        return [os.path.basename(name) for name in names]

    def set_unit_name(self, x_name=None, y_name=None):
        if x_name:
            self.__x_unit_name = x_name
        if y_name:
            self.__y_unit_name = y_name

    def emit_updated(self):
        if not self.__locked:
            self.sigUpdated.emit(self.export())

    def observe_boundaries_change(self):
        new_xmin, new_xmax, new_res = self.bound_x()
        if new_xmin != self.__x_min or new_xmax != self.__x_max or new_res != self.__x_res:
            self.__x_min = new_xmin
            self.__x_max = new_xmax
            self.__x_res = new_res
            self.sigBoundaries.emit(new_xmin, new_xmax, new_res)

    def add_data_files(self, names):
        names = self._purify_names(names)
        self.log.emit('Ranges: loading data files...')
        added_names_dict = ranges.Ranges.add_data_files(self, names)
        if added_names_dict:
            self._add_unique_names(added_names_dict)
            basenames = self.__make_basenames(added_names_dict.values())
            self.sigAdded.emit(basenames)
            self.observe_boundaries_change()
            self.emit_updated()
        self.log.emit('Ranges: done')

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.observe_boundaries_change()
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self._remove_unique_name(index)
            self.observe_boundaries_change()
            self.emit_updated()

    def update(self, index, arr):
        new_index = ranges.Ranges.update(self, index, arr)
        if index != new_index:
            self.sigAdded.emit([])
        self.observe_boundaries_change()
        self.emit_updated()

    def set_visibility(self, index, flag):
        ranges.Ranges.set_visibility(self, index, flag)
        self.emit_updated()

    def __add_unit_names(self, info_dict):
        new_info_dict = {}
        for key, value in info_dict.items():
            newvalue = value
            if 'X' in key:
                newvalue = str(value) + ' ' + str(self.__x_unit_name)
            elif 'Y' in key:
                newvalue = str(value) + ' ' + str(self.__y_unit_name)
            new_info_dict[key] = newvalue
        return new_info_dict

    def get_settings(self, index):
        info_dict = self.make_info(index)
        info_dict = self.__add_unit_names(info_dict)
        self.sigInfo.emit(info_dict)

    def lock(self, flag):
        if flag:
            self.__locked = True
        else:
            self.__locked = False
            self.emit_updated()


