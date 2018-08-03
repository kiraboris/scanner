

import os.path

from gui import panoram
from gui.pyqtgraph.Qt import QtGui, QtCore

Application = QtGui.QApplication


class ExpDock(QtGui.QDockWidget):

    sigAddItems = QtCore.Signal(list)
    sigRemoveItem = QtCore.Signal(int)
    sigItemChecked = QtCore.Signal(int, bool)

    def __init__(self):
        QtGui.QDockWidget.__init__(self, "Experimental data")
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
        self.__filenames = []

    def confirmAddingItems(self, names):
        for name in names:
            self._addItem(os.path.basename(name))
            self.__filenames.append(name)

    def _purifyFileNames(self, names):
        newNames = []
        for fileName in names:
            if fileName not in self.__filenames:
                newNames.append(fileName)
        return newNames

    def _addButtonClick(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, 'Add experimetal data file(s)...')
        fileNames = fileNames[0]
        if fileNames:
            newNames = self._purifyFileNames(fileNames)
            if newNames:
                self.sigAddItems.emit(newNames)

    def _addItem(self, name):
        item = QtGui.QListWidgetItem(name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        #check_box = self.listWidget.itemWidget(item)
        #check_box.stateChanged.connect(self._itemChecked2)

    def _removeButtonClick(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        if item:
            self.sigRemoveItem.emit(row)
            del self.__filenames[row]
            item = None

    def _itemChecked(self, item):
        row = self.listWidget.row(item)
        self.sigItemChecked.emit(row, item.checkState() == QtCore.Qt.Checked)


class MainWindow(QtGui.QMainWindow):

    #sigClearExpTiggered = QtCore.Signal(object)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Scanner')
        self.resize(1200, 600)

        self.pan = panoram.Panoram()
        self.expDock = ExpDock()
        #self.simDock = SimDock()

        self.setCentralWidget(self.pan.widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.expDock)

        self._createMainMenu()

        #data = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
        #self.pan.plotUpper(data, pen="m")
        #self.pan.plotLower(data, pen="0ff")
        #self.pan.setRegion([1800, 2000])


    def _createMainMenu(self):

        menu = self.menuBar()

        fileMenu = menu.addMenu("&File")
        newAction = QtGui.QAction("&New project", self)
        openAction = QtGui.QAction("&Open project...", self)
        saveAction = QtGui.QAction("&Save project", self)
        saveAsAction = QtGui.QAction("Save project as...", self)
        exitAction = QtGui.QAction("&Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)


        winMenu = menu.addMenu("&Window")
        showExpWinAction = QtGui.QAction("&Experimental data...", self)
        showExpWinAction.triggered.connect(self.expDock.show)
        winMenu.addAction(showExpWinAction)




        #simMenu = menu.addMenu("&Simulation")

    #def _clearExpTrigger(self):
    #    self.pan.clearUpper()
    #    self.sigClearExpTiggered.emit(self)




#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0

#label = pg.LabelItem(justify='right')




#cross hair
#vLine = pg.InfiniteLine(angle=90, movable=False)
#hLine = pg.InfiniteLine(angle=0, movable=False)
#p1.addItem(vLine, ignoreBounds=True)
#p1.addItem(hLine, ignoreBounds=True)


#vb = p1.getViewBox()


#def mouseMoved(evt):
#    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
#    if p1.sceneBoundingRect().contains(pos):
#        mousePoint = vb.mapSceneToView(pos)
#        index = int(np.round(mousePoint.x()))
#        if index > 0 and index < len(data):
#            label.setText("<span style='font-size: 12pt'>Frequency=%0.2f, "
#                          "  <span style='color: magenta'>Intensity=%0.2f</span>"
#                          % (mousePoint.x(), data[index]))
        #vLine.setPos(mousePoint.x())
        #hLine.setPos(mousePoint.y())



#proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)

