
import os.path

from gui.pyqtgraph.Qt import QtCore
from entities import ranges
from . import unique_name_holder


class RangesWrapper(QtCore.QObject, ranges.Ranges, unique_name_holder.UniqueNameHolder):

    sigUpdated = QtCore.Signal(object)
    sigAdded = QtCore.Signal(list)
    sigInfo = QtCore.Signal(dict)

    def __init__(self, parent=None, **kwargs):
        QtCore.QObject.__init__(self, parent)
        ranges.Ranges.__init__(self, **kwargs)
        unique_name_holder.UniqueNameHolder.__init__(self)
        self.__x_unit_name = "MHz"
        self.__y_unit_name = "arb"

    @staticmethod
    def __make_basenames(names):
        return [os.path.basename(name) for name in names]

    def set_unit_name(self, x_name=None, y_name=None):
        if x_name:
            self.__x_unit_name = x_name
        if y_name:
            self.__y_unit_name = y_name

    def emit_updated(self):
        self.sigUpdated.emit(self.export())

    def add_data_files(self, names):
        names = self._purify_names(names)
        added_names_dict = ranges.Ranges.add_data_files(self, names)
        if added_names_dict:
            self._add_unique_names(added_names_dict)
            basenames = self.__make_basenames(added_names_dict.values())
            self.sigAdded.emit(basenames)
            self.emit_updated()

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self._remove_unique_name(index)
            self.emit_updated()

    def update(self, index, arr):
        new_index = ranges.Ranges.update(self, index, arr)
        if index != new_index:
            self.sigAdded.emit([])
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


