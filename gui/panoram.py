
from . import pyqtgraph as pg
from gui.pyqtgraph.Qt import QtGui, QtCore


class Panoram:
    def __init__(self, parent=None):
        self.widget = pg.GraphicsLayoutWidget(parent)

        self.__p1 = self.widget.addPlot(row=1, col=0)
        self.__p2 = self.widget.addPlot(row=2, col=0)
        self.__p3 = self.widget.addPlot(row=3, col=0)

        font = QtGui.QFont()
        font.setPixelSize(14)
        self.__p2.getAxis('bottom').tickFont=font
        self.__p2.getAxis('bottom').setStyle(tickTextOffset=7)

        self.widget.centralWidget.layout.setRowStretchFactor(2, 4)
        self.widget.centralWidget.layout.setRowStretchFactor(3, 4)

        self.__region = pg.LinearRegionItem()
        self.__region.setZValue(10)
        self.__region.setMovable(m=True, lm=False)
        self.__region.sigRegionChanged.connect(self._updateRanges)
        self.__p1.addItem(self.__region, ignoreBounds=True)

        self._setupMasterPlot(self.__p1)
        self._setupSlavePlot(self.__p2)
        self._setupSlavePlot(self.__p3)

    def setConfig(self, config):
        self.widget.setBackground(config['plot_background_color'])
        for plot in [self.__p1, self.__p2, self.__p3]:
            plot.getAxis('bottom').setPen(color=config['plot_axes_color'])
            plot.getAxis('left').setPen(color=config['plot_axes_color'])

    def _setupSlavePlot(self, plot):
        plot.setAutoVisible(y=True)
        plot.hideButtons()
        plot.setMenuEnabled(enableMenu=False, enableViewBoxMenu=True)
        plot.sigRangeChanged.connect(self._updateRegion)

    def _setupMasterPlot(self, plot):
        plot.hideButtons()
        plot.setMenuEnabled(enableMenu=False, enableViewBoxMenu=True)
        plot.getViewBox().sigMouseClick.connect(self._setRegionCenter)

    def plotUpper(self, data, pen="ccc"):
        self.clearUpper()
        if data is not None:
            self.__p1.plot(data, pen=pen)
            self.__p1.getViewBox().autoRange()
            self.__p2.plot(data, pen=pen)

    def plotLower(self, data, pen="ccc"):
        self.clearLower()
        if data is not None:
            self.__p3.plot(data, pen=pen)

    def clearUpper(self):
        self.__p1.clearPlots()
        self.__p2.clearPlots()

    def clearLower(self):
        self.__p3.clearPlots()

    def setRegion(self, rgn):
        self.__region.setRegion(rgn)

    def _setRegionCenter(self, pos):
        minX, maxX = self.__region.getRegion()
        width = maxX - minX
        newRegion = (pos.x() - width / 2, pos.x() + width / 2)
        self.__region.setRegion(newRegion)

    def _updateRanges(self):
        self.__region.setZValue(10)
        minX, maxX = self.__region.getRegion()
        self.__p2.setXRange(minX, maxX, padding=0)
        self.__p3.setXRange(minX, maxX, padding=0)

    def _updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.__region.setRegion(rgn)