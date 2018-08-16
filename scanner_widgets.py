
from gui import panoram, list_dock, table_dock
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

    sigApplySettings = QtCore.Signal(int, dict)

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

    def apply_settings_proxy(self, params_dict):
        self.sigApplySettings.emit(self.currentRow(), params_dict)


class RotorParamDock(list_dock.ListDock):
    def __init__(self):
        list_dock.ListDock.__init__(self, "Rotor")
        self.addButton.setVisible(False)
        self.removeButton.setVisible(False)
        font = QtGui.QFont("Monospace")
        font.setStyleHint(QtGui.QFont.Monospace)
        self.listWidget.setFont(font)

    def _addButtonClick(self):
        pass

    def setTitle(self, name):
        self.setWindowTitle('Rotor: ' + name)


class AutofitDock(QtGui.QDockWidget):
    def __init__(self):
        QtGui.QDockWidget.__init__(self, "Autofit")

        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        check1 = QtGui.QCheckBox("Auto select transitions to fit")
        check1.stateChanged.connect(self._setOption1)
#        check1.setChecked(False)
        layout.addWidget(check1, 0, 0, 1, 2)

        self.label1 = QtGui.QLabel()
        self.label1.setWordWrap(True)
        layout.addWidget(self.label1, 1, 0, 1, 2)
        check1.setCheckState(QtCore.Qt.Checked)


        check2 = QtGui.QCheckBox("Auto choose rotor params to float")
        check2.stateChanged.connect(self._setOption2)
        layout.addWidget(check2, 2, 0, 1, 2)

        self.label2 = QtGui.QLabel()
        self.label2.setWordWrap(True)
        layout.addWidget(self.label2, 3, 0, 1, 2)
        check2.setCheckState(QtCore.Qt.Checked)

        check3 = QtGui.QCheckBox("Auto add rotor params")
        check3.stateChanged.connect(self._setOption3)
        layout.addWidget(check3, 4, 0, 1, 2)

        self.label3 = QtGui.QLabel()
        self.label3.setWordWrap(True)
        layout.addWidget(self.label3, 5, 0, 1, 2)
        check3.setCheckState(QtCore.Qt.Checked)

        self.fitButton = QtGui.QPushButton('Fit')
        #self.addButton.clicked.connect(self._addButtonClick)
        self.undoButton = QtGui.QPushButton('Undo')
        #self.removeButton.clicked.connect(self._removeButtonClick)
        layout.addWidget(self.fitButton, 6, 0)
        layout.addWidget(self.undoButton, 6, 1)

        self.chooseWidget = QtGui.QListWidget()
        layout.addWidget(self.chooseWidget, 7, 0, 1, 2)

        widget.setLayout(layout)
        self.setWidget(widget)

    def setTitle(self, name):
        self.setWindowTitle('Autofit: ' + name)

    def _setOption1(self, state):
        checked = (state == QtCore.Qt.Checked)
        if checked:
            self.label1.setText("J-groups and K-groups of transitions will be selected and assigned automatically. "
                                "Manual selection will be ignored. J, K will be increased gradually.")
        else:
            self.label1.setText("Manual selection from Simulation and Transitions panes will be used for"
                                " automatic assignment (what you see is what you get).")

    def _setOption2(self, state):
        checked = (state == QtCore.Qt.Checked)
        if checked:
            self.label2.setText("A test will be run to see which parameters do affect selected transitions.")
        else:
            self.label2.setText("Manual selection from the Rotor pane will be used.")

    def _setOption3(self, state):
        checked = (state == QtCore.Qt.Checked)
        if checked:
            self.label3.setText("Based on resiual trends, higher order distortion parameters will be possibly added "
                                "automatically.")
        else:
            self.label3.setText("Distortions are not added automatically. "
                                "You can add them manually in the Rotor pane.")


class LogDock(QtGui.QDockWidget):
    def __init__(self):
        QtGui.QDockWidget.__init__(self, "Log")

        widget = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        layout.setMargin(2)

        self.logWidget = QtGui.QPlainTextEdit()
        self.logWidget.setReadOnly(True)
        layout.addWidget(self.logWidget, 0, 0)

        widget.setLayout(layout)
        self.setWidget(widget)

    def log(self, message):
        self.logWidget.appendPlainText(message)
        self.logWidget.verticalScrollBar().setValue(self.logWidget.verticalScrollBar().maximum())
        self.logWidget.repaint()


class SimSettingsDock(table_dock.TableDock):

    def __init__(self):
        table_dock.TableDock.__init__(self, "Simulation")

    def setTitle(self, name):
        self.setWindowTitle('Simulation: ' + name)


class MainWindow(QtGui.QMainWindow):

    #sigClearExpTiggered = QtCore.Signal(object)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Scanner')
        self.resize(1400, 700)

        self.pan = panoram.Panoram()
        self.expDock = ExpDock()
        self.simDock = SimDock()
        self.parDock = RotorParamDock()
        self.fitDock = AutofitDock()
        self.logDock = LogDock()
        self.stgDock = SimSettingsDock()

        self.setCentralWidget(self.pan.widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.expDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.simDock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.stgDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.parDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.fitDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.logDock)

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
        exitAction = QtGui.QAction("E&xit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)


        winMenu = menu.addMenu("&Window")
        action = QtGui.QAction("E&xperiments", self)
        action.triggered.connect(self.expDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Models", self)
        action.triggered.connect(self.simDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Rotor params", self)
        action.triggered.connect(self.parDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Simulation params", self)
        action.triggered.connect(self.stgDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Autofit", self)
        action.triggered.connect(self.fitDock.show)
        winMenu.addAction(action)
        action = QtGui.QAction("&Log", self)
        action.triggered.connect(self.logDock.show)
        winMenu.addAction(action)

    def log(self, message):
        self.logDock.log(message)

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

