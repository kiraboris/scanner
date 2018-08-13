
from gui import panoram, list_dock, table_dialog
from gui.pyqtgraph.Qt import QtGui, QtCore

Application = QtGui.QApplication


class ExpDock(list_dock.ListDock):
    def __init__(self):
        list_dock.ListDock.__init__(self, "Experiments")

    def _addButtonClick(self):
        filter = "Plain data (*.dat, *.txt);;All files (*.*)"
        file_names = QtGui.QFileDialog.getOpenFileNames(self,
                                                        'Add experimetal data file(s)...',
                                                        filter=filter)
        file_names = file_names[0]
        if file_names:
            self.sigAddItems.emit(file_names)


class SimDock(list_dock.ListDock):
    def __init__(self):
        list_dock.ListDock.__init__(self, "Models")

    def _addButtonClick(self):
        filter = "Pickett (*.par, *.var, *.int);;All files (*.*)"
        file_name = QtGui.QFileDialog.getOpenFileName(self,
                                                      'Add quantum model...',
                                                      filter=filter)
        file_name = file_name[0]
        if file_name:
            self.sigAddItem.emit(file_name)


class MainWindow(QtGui.QMainWindow):

    #sigClearExpTiggered = QtCore.Signal(object)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Scanner')
        self.resize(1200, 600)

        self.pan = panoram.Panoram()
        self.expDock = ExpDock()
        self.simDock = SimDock()
        self.expSettings = table_dialog.TableDialog()
        self.simSettings = table_dialog.TableDialog()

        self.setCentralWidget(self.pan.widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.expDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.simDock)

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
        action = QtGui.QAction("&Experiments", self)
        action.triggered.connect(self.expDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Models", self)
        action.triggered.connect(self.simDock.show)
        winMenu.addAction(action)



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

