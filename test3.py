
from gui import scanner
from gui.pyqtgraph.Qt import QtGui, QtCore
import sys

if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()