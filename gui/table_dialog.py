
from .pyqtgraph.Qt import QtCore, QtGui


class TableDialog(QtGui.QDialog):

    sigSheetChanged = QtCore.Signal(int, dict)

    def __init__(self):
        QtGui.QDialog.__init__(self)
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()

        layout.addWidget(self.tableWidget, 0, 0, 1, 2)

        saveButton = QtGui.QPushButton('Save')
        saveButton.clicked.connect(self._emitSheet)
        rejectButton = QtGui.QPushButton('Reject')
        rejectButton.clicked.connect(self.close)
        layout.addWidget(saveButton, 1, 0)
        layout.addWidget(rejectButton, 1, 1)

        self.setLayout(layout)
        self.setModal(True)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.__saved_index = None

    def _emitSheet(self):
        self.hide()
        self.sigSheetChanged.emit(self.__saved_index, {})

    def setSheet(self, index, name, props_dict):
        self.__saved_index = index
        self.setWindowTitle(name)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(props_dict))
        self.tableWidget.setColumnCount(2)
        for row, (key, value) in enumerate(props_dict.items()):
            nameitem = QtGui.QTableWidgetItem(key)
            nameitem.setFlags(nameitem.flags() ^ QtCore.Qt.ItemIsEditable)
            codeitem = QtGui.QTableWidgetItem(value)
            self.tableWidget.setItem(row, 0, nameitem)
            self.tableWidget.setItem(row, 1, codeitem)
