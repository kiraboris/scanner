
from gui.scannerwindow import ScannerWindow
from gui.pyqtgraph.Qt import QtGui, QtCore
import sys

app = QtGui.QApplication([])
win = ScannerWindow()
win.show()

#if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
sys.exit(app.exec_())
