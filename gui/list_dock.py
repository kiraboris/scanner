
from .pyqtgraph.Qt import QtCore, QtGui
from abc import ABC, abstractmethod


class ListDock(QtGui.QDockWidget):

    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)
    sigItemChecked = QtCore.Signal(int, bool)

    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()

        self.listWidget = QtGui.QListWidget()
        self.listWidget.itemChanged.connect(self._itemChecked)

        addButton = QtGui.QPushButton('Add...')
        addButton.clicked.connect(self._addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self._removeButtonClick)

        layout.addWidget(self.listWidget, 0, 0, 1, 2)
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(removeButton, 1, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    @abstractmethod
    def _addButtonClick(self):
        pass

    def _removeButtonClick(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        if item:
            self._removeItem(item, row)
            item = None

    def _addItem(self, name):
        item = QtGui.QListWidgetItem(name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)

    def _removeItem(self, item, row):
        self.sigRemoveItem.emit(row)

    def _itemChecked(self, item):
        row = self.listWidget.row(item)
        self.sigItemChecked.emit(row, item.checkState() == QtCore.Qt.Checked)
