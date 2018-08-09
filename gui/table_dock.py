
from .pyqtgraph.Qt import QtCore, QtGui


class TableInfoDock(QtGui.QDockWidget):
    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.tableWidget = QtGui.QTableWidget()

        layout.addWidget(self.tableWidget, 0, 0, 1, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    def writeInfo(self):
        pass
