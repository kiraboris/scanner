
from gui.pyqtgraph.Qt import QtCore
from entities import ranges


class RangesWrapper(QtCore.QObject, ranges.Ranges):

    sigUpdated = QtCore.Signal(object)
    sigAdded = QtCore.Signal(list)

    def emit_updated(self):
        self.sigUpdated.emit(self.export())

    def add_data_files(self, names):
        addedNames = ranges.Ranges.add_data_files(self, names)
        if addedNames:
            self.sigAdded.emit(addedNames)
            self.emit_updated()

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self.emit_updated()

    def set_visibility(self, index, flag):
        ranges.Ranges.set_visibility(self, index, flag)
        self.emit_updated()

