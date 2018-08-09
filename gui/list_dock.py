
from .pyqtgraph.Qt import QtCore, QtGui
from abc import ABC, abstractmethod


class ListDock(QtGui.QDockWidget):

    sigAddItem = QtCore.Signal(str)
    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)

    sigItemChecked = QtCore.Signal(int, bool)
    sigItemNameChanged = QtCore.Signal(int, str)
    sigCurrentRowChanged = QtCore.Signal(int)

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
        style = ("QTableView"
                "{{"
               # "color: {color};"
                "background: {color};"
                #"}}"
                #"QTableView::item"
                #"{{"
               # "background: {color};"
                "}}".format(color="#eee"))
        self.tableWidget.setStyleSheet(style)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        layout.addWidget(self.tableWidget, 1, 0, 1, 2)

        #self.setInfoSheet({'item': 'value'})

        addButton = QtGui.QPushButton('Add')
        addButton.clicked.connect(self._addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(addButton, 2, 0)
        layout.addWidget(removeButton, 2, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    def setInfoSheet(self, props_dict):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(props_dict))
        self.tableWidget.setColumnCount(2)
        for row, (key, value) in enumerate(props_dict.items()):
            nameitem = QtGui.QTableWidgetItem(key)
            codeitem = QtGui.QTableWidgetItem(value)
            self.tableWidget.setItem(row, 0, nameitem)
            self.tableWidget.setItem(row, 1, codeitem)

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

