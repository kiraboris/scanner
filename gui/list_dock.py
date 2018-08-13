
from .pyqtgraph.Qt import QtCore, QtGui
from abc import ABC, abstractmethod


class ListDock(QtGui.QDockWidget):

    sigAddItem = QtCore.Signal(str)
    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)

    sigItemChecked = QtCore.Signal(int, bool)
    sigItemNameChanged = QtCore.Signal(int, str)
    sigCurrentRowChanged = QtCore.Signal(int)

    sigSettingsRequest = QtCore.Signal(int, str)

    def __init__(self, dock_name):
        QtGui.QDockWidget.__init__(self, dock_name)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.itemChanged.connect(self._itemChanged)
        self.listWidget.currentRowChanged.connect(self.sigCurrentRowChanged)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.ctxMenu)
        layout.addWidget(self.listWidget, 0, 0, 1, 2)

        addButton = QtGui.QPushButton('Add')
        addButton.clicked.connect(self._addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(removeButton, 1, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    @abstractmethod
    def _addButtonClick(self):
        pass

    def renameCurrentItem(self):
        cur = self.listWidget.currentItem()
        self.listWidget.editItem(cur)

    def emitSettingsRequest(self):
        cur = self.listWidget.currentItem()
        row = self.listWidget.row(cur)
        name = cur.text()
        self.sigSettingsRequest.emit(row, name)

    def ctxMenu(self, point):
        cur = self.listWidget.currentItem()
        if not cur:
            return

        menu = QtGui.QMenu(self)
        renameAction = QtGui.QAction("Rename", self)
        renameAction.triggered.connect(self.renameCurrentItem)
        menu.addAction(renameAction)
        menu.addSeparator()
        settingsAction = QtGui.QAction("Settings && Info...", self)
        settingsAction.triggered.connect(self.emitSettingsRequest)
        menu.addAction(settingsAction)

        parentPosition = self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        menu.move(parentPosition + point)
        menu.show()

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

