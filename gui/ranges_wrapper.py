
from .pyqtgraph.Qt import QtCore
from entities import ranges
import os.path

class RangesWrapper(QtCore.QObject, ranges.Ranges):

    sigUpdated = QtCore.Signal(object)
    sigAdded = QtCore.Signal(list)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        ranges.Ranges.__init__(self)
        self.__filenames = {}
        self.__flag_files_unque = True

    def __purify_names(self, names):
        new_names = []
        for file_name in names:
            if file_name not in self.__filenames.values():
                new_names.append(file_name)
        return new_names

    @staticmethod
    def __make_basenames(names):
        return [os.path.basename(name) for name in names]

    def set_files_unique_flag(self, flag):
        self.__flag_files_unque = flag

    def emit_updated(self):
        self.sigUpdated.emit(self.export())

    def add_data_files(self, names):
        if self.__flag_files_unque:
            names = self.__purify_names(names)
        added_names_dict = ranges.Ranges.add_data_files(self, names)
        if added_names_dict:
            self.__filenames.update(added_names_dict)
            basenames = self.__make_basenames(added_names_dict.values())
            self.sigAdded.emit(basenames)
            self.emit_updated()

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self.__filenames.pop(index, None)
            self.emit_updated()

    def set_visibility(self, index, flag):
        ranges.Ranges.set_visibility(self, index, flag)
        self.emit_updated()

