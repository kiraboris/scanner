
import sys
from scanner.scannergui import MainWindow
from gui.pyqtgraph.Qt import QtGui, QtCore
from entities import ranges


class RangesWrapper(ranges.Ranges):

    sigUpdated = QtCore.Signal(object, object)

    def emit_updated(self):
        self.sigUpdated.emit(self, self.export())

    def add_data_file(self, name):
        if ranges.Ranges.add_data_file(self, name):
            self.emit_updated()

    def deserialize(self, stream):
        if ranges.Ranges.deserialize(self, stream):
            self.emit_updated()

    def remove(self, index):
        if ranges.Ranges.remove(self, index):
            self.emit_updated()



