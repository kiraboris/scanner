
import sys

from gui.pyqtgraph.Qt import QtCore
from entities import ranges


class RangesWrapper(QtCore.QObject, ranges.Ranges):

    sigUpdated = QtCore.Signal(object)

    def emit_updated(self):
        self.sigUpdated.emit(self.export())

    def add_data_file(self, name):
        if ranges.Ranges.add_data_file(self, name):
            self.emit_updated()

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self.emit_updated()



