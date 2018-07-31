

from ..gui import panoram
from ..gui.pyqtgraph.Qt.QtGui import QApplication

Application = QApplication


class ExpDock(QtGui.QDockWidget):

    sigAddFile = QtCore.Signal(object)

    def __init__(self):
        QtGui.QDockWidget.__init__(self, "Experimental data")
        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()

        self.listWidget = QtGui.QListWidget()
        addButton = QtGui.QPushButton('Add...')
        addButton.clicked.connect(self.addButtonClick)
        removeButton = QtGui.QPushButton('Remove')
        removeButton.clicked.connect(self.removeButtonClick)

        layout.addWidget(self.listWidget, 0, 0, 1, 2)
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(removeButton, 1, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    def addButtonClick(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Add experimetal data')
        if fileName:
            self.sigAddFile.emit(fileName[0])

    def addItem(self, name):
        item = QtGui.QListWidgetItem(name, self.listWidget)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def removeButtonClick(self):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None


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

