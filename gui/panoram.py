
from . import pyqtgraph as pg

class Panoram(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)

        self.__p1 = self.addPlot(row=1, col=0)
        self.__p2 = self.addPlot(row=2, col=0)
        self.__p3 = self.addPlot(row=3, col=0)

        self.centralWidget.layout.setRowStretchFactor(2, 3)
        self.centralWidget.layout.setRowStretchFactor(3, 3)

        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.region.setMovable(m=True, lm=False)
        self.region.sigRegionChanged.connect(self._updateRanges)
        self.__p1.addItem(self.region, ignoreBounds=True)

        self._setupMasterPlot(self.__p1)
        self._setupSlavePlot(self.__p2)
        self._setupSlavePlot(self.__p3)

    def _setupSlavePlot(self, plot):
        plot.setAutoVisible(y=True)
        plot.hideButtons()
        plot.setMenuEnabled(enableMenu=False, enableViewBoxMenu=True)
        plot.sigRangeChanged.connect(self._updateRegion)

    def _setupMasterPlot(self, plot):
        plot.hideButtons()
        plot.setMenuEnabled(enableMenu=False, enableViewBoxMenu=True)
        plot.getViewBox().sigMouseClick.connect(self._setRegionCenter)

    def plotUpper(self, **kwargs):
        self.__p1.plot(kwargs)
        self.__p2.plot(kwargs)

    def plotLower(self, **kwargs):
        self.__p3.plot(kwargs)

    def _setRegionCenter(self, pos):
        minX, maxX = self.region.getRegion()
        width = maxX - minX
        newRegion = (pos.x() - width / 2, pos.x() + width / 2)
        self.region.setRegion(newRegion)

    def _updateRanges(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.__p1.setXRange(minX, maxX, padding=0)
        self.__p2.setXRange(minX, maxX, padding=0)
        self.__p3.setXRange(minX, maxX, padding=0)

    def _updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)