
from .pyqtgraph.Qt import QtCore, QtGui
from abc import ABC, abstractmethod


class ListDock(QtGui.QDockWidget):

    sigAddItem = QtCore.Signal(str)
    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)

    sigItemChecked = QtCore.Signal(int, bool)
    sigItemNameChanged = QtCore.Signal(int, str)
    sigCurrentRowChanged = QtCore.Signal(int)

    sigSheetChanged = QtCore.Signal(int, dict)
    sigSheetRejected = QtCore.Signal(int)

    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.itemChanged.connect(self._itemChanged)
        self.listWidget.currentRowChanged.connect(self.sigCurrentRowChanged)
        layout.addWidget(self.listWidget, 0, 0, 1, 2)

        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.itemChanged.connect(self._enableSheetButtons)

        addButton = QtGui.QPushButton('Add')
        addButton.clicked.connect(self._addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(removeButton, 1, 1)

        layout.addWidget(self.tableWidget, 2, 0, 1, 2)

        self.saveButton = QtGui.QPushButton('Apply')
        self.saveButton.clicked.connect(self._emitSheetChanged)
        self.rejectButton = QtGui.QPushButton('Revert')
        self.rejectButton.clicked.connect(self._emitSheetRejected)
        layout.addWidget(self.saveButton, 3, 0)
        layout.addWidget(self.rejectButton, 3, 1)
        self._disableSheetButtons()

        widget.setLayout(layout)
        self.setWidget(widget)

    @abstractmethod
    def _addButtonClick(self):
        pass

    def _removeButtonClick(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        if item:
            self.removeItem(row)
            item = None

    def addItem(self, name):
        item = QtGui.QListWidgetItem(name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        if(self.listWidget.currentRow() < 0):
            self.listWidget.setCurrentRow(0)

    def addItems(self, names):
        for name in names:
            self.addItem(name)

    def removeItem(self, row):
        self.sigRemoveItem.emit(row)

    def _itemChanged(self, item):
        row = self.listWidget.row(item)
        self.sigItemChecked.emit(row, item.checkState() == QtCore.Qt.Checked)
        self.sigItemNameChanged.emit(row, item.text())

    def _emitSheetRejected(self):
        self.sigSheetRejected.emit(self.listWidget.currentRow())

    def _emitSheetChanged(self):
        new_props = {}
        for row in range(0, self.tableWidget.rowCount()):
            twi0 = self.tableWidget.item(row, 0)
            twi1 = self.tableWidget.item(row, 1)
            new_props[twi0.text()] = twi1.text()
        self.sigSheetChanged.emit(self.listWidget.currentRow(), new_props)

    def setSheet(self, props_dict):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(props_dict))
        self.tableWidget.setColumnCount(2)
        for row, (key, value) in enumerate(props_dict.items()):
            nameitem = QtGui.QTableWidgetItem(key)
            nameitem.setFlags(nameitem.flags() ^ QtCore.Qt.ItemIsEditable)
            codeitem = QtGui.QTableWidgetItem(value)
            self.tableWidget.setItem(row, 0, nameitem)
            self.tableWidget.setItem(row, 1, codeitem)
        self._disableSheetButtons()

    def _enableSheetButtons(self):
        self.saveButton.setEnabled(True)
        self.rejectButton.setEnabled(True)

    def _disableSheetButtons(self):
        self.saveButton.setEnabled(False)
        self.rejectButton.setEnabled(False)

