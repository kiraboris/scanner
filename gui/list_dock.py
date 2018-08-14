
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

    def __init__(self, dock_name, flag_table=True):
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
        self.tableWidget.itemChanged.connect(self._emitSheetChanged)
        if not flag_table:
            self.tableWidget.setVisible(False)

        addButton = QtGui.QPushButton('Add')
        addButton.clicked.connect(self._addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(removeButton, 1, 1)

        layout.addWidget(self.tableWidget, 2, 0, 1, 2)

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

    def addItem(self, name, flag_checked=True):
        item = QtGui.QListWidgetItem(name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
        if flag_checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

        self.listWidget.addItem(item)
        if self.listWidget.currentRow() < 0:
            self.listWidget.setCurrentRow(0)

    def addItems(self, names, checked_dict=None):
        for i, name in enumerate(names):
            if checked_dict:
                self.addItem(name, checked_dict.get(i, False))
            else:
                self.addItem(name)

    def setItems(self, names, checked_dict=None):
        self.listWidget.clear()
        self.addItems(names, checked_dict)

    def removeItem(self, row):
        self.sigRemoveItem.emit(row)

    def _itemChanged(self, item):
        row = self.listWidget.row(item)
        self.sigItemChecked.emit(row, item.checkState() == QtCore.Qt.Checked)
        self.sigItemNameChanged.emit(row, item.text())

    def _emitSheetChanged(self):
        cur_row = self.listWidget.currentRow()
        if cur_row >= 0:
            new_props = {}
            for row in range(0, self.tableWidget.rowCount()):
                twi0 = self.tableWidget.item(row, 0)
                twi1 = self.tableWidget.item(row, 1)
                new_props[twi0.text()] = twi1.text()
            self.sigSheetChanged.emit(cur_row, new_props)

    def setSheet(self, props_dict):
        self.tableWidget.itemChanged.disconnect(self._emitSheetChanged)

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(props_dict))
        self.tableWidget.setColumnCount(2)
        for row, (key, value) in enumerate(props_dict.items()):
            nameitem = QtGui.QTableWidgetItem(key)
            nameitem.setFlags(nameitem.flags() ^ QtCore.Qt.ItemIsEditable)
            codeitem = QtGui.QTableWidgetItem(value)
            self.tableWidget.setItem(row, 0, nameitem)
            self.tableWidget.setItem(row, 1, codeitem)

        self.tableWidget.itemChanged.connect(self._emitSheetChanged)




