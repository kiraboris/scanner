
from .pyqtgraph.Qt import QtCore, QtGui


class TableDock(QtGui.QDockWidget):

    sigSheetChanged = QtCore.Signal(dict)

    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.itemChanged.connect(self._emitSheetChanged)

        layout.addWidget(self.tableWidget, 0, 0, 1, 2)

        widget.setLayout(layout)
        self.setWidget(widget)

    def _emitSheetChanged(self):
        new_props = {}
        for row in range(0, self.tableWidget.rowCount()):
            twi0 = self.tableWidget.item(row, 0)
            twi1 = self.tableWidget.item(row, 1)
            if twi1.flags() & QtCore.Qt.ItemIsUserCheckable:
                new_props[twi0.text()] = (twi1.checkState() == QtCore.Qt.Checked)
            else:
                new_props[twi0.text()] = twi1.text()
        self.sigSheetChanged.emit(new_props)

    def setSheet(self, props_dict):
        self.tableWidget.itemChanged.disconnect(self._emitSheetChanged)

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(props_dict))
        self.tableWidget.setColumnCount(2)
        for row, (key, value) in enumerate(props_dict.items()):
            nameitem = QtGui.QTableWidgetItem(key)
            nameitem.setFlags(nameitem.flags() ^ QtCore.Qt.ItemIsEditable)
            codeitem = QtGui.QTableWidgetItem()
            if isinstance(value, bool):
                codeitem.setFlags(codeitem.flags() ^ QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
                if value:
                    codeitem.setCheckState(QtCore.Qt.Checked)
                else:
                    codeitem.setCheckState(QtCore.Qt.Unchecked)
            else:
                codeitem.setFlags(codeitem.flags() ^ QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable )
                codeitem.setText(value)
            self.tableWidget.setItem(row, 0, nameitem)
            self.tableWidget.setItem(row, 1, codeitem)

        self.tableWidget.itemChanged.connect(self._emitSheetChanged)

