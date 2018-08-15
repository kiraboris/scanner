
from .pyqtgraph.Qt import QtCore, QtGui
from abc import ABC, abstractmethod


class SpecialListDelegate(QtGui.QItemDelegate):
    def sizeHint(self, option, index):
        sz = QtGui.QItemDelegate.sizeHint(self, option, index)
        sz.setHeight(sz.height() * 1.5)
        return sz


class ListDock(QtGui.QDockWidget):

    sigAddItem = QtCore.Signal(str)
    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)

    sigItemChecked = QtCore.Signal(int, bool)
    sigItemNameChanged = QtCore.Signal(int, str)
    sigCurrentRowChanged = QtCore.Signal(int)
    sigCurrentTextChanged = QtCore.Signal(str)

    sigSheetChanged = QtCore.Signal(int, dict)

    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.itemChanged.connect(self._itemChanged)
        self.listWidget.currentRowChanged.connect(self.sigCurrentRowChanged)
        self.listWidget.currentTextChanged.connect(self.sigCurrentTextChanged)
        self.listWidget.setItemDelegate(SpecialListDelegate())
        layout.addWidget(self.listWidget, 0, 0, 1, 2)

        self.addButton = QtGui.QPushButton('Add')
        self.addButton.clicked.connect(self._addButtonClick)
        self.removeButton = QtGui.QPushButton('Remove')
        self.removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(self.addButton, 1, 0)
        layout.addWidget(self.removeButton, 1, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    def currentRow(self):
        return self.listWidget.currentRow()

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


