"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows 
the mouse.


"""

#import initExample ## Add path to library (just for examples; you do not need this)
import numpy as np
from . import pyqtgraph as pg
from .pyqtgraph.Qt import QtGui, QtCore

#pg.setConfigOption('background', 'w')

#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow(size=(1000, 500))
win.setWindowTitle('scanner')
label = pg.LabelItem(justify='right')

p1 = win.addPlot(row=2, col=0)
p2 = win.addPlot(row=1, col=0)
win.centralWidget.addItem(label, row=3, col=0)
win.centralWidget.layout.setRowStretchFactor(2,2)



region = pg.LinearRegionItem()
region.setZValue(10)
region.setMovable(m=True, lm=False)


# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this 
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)

#pg.dbg()
p1.setAutoVisible(y=True)
p1.setMouseEnabled(True)


#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

p1.plot(data, pen="m")

p2.plot(data, pen="m")

#p2.autoRange(True)

def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)

    p2range = p2.viewRange()
    if p2range[0][0] > minX:
        p2.setXRange(minX, p2range[0][1] - (p2range[0][0] - minX), padding=0)
    elif p2range[0][1] < maxX:
        p2.setXRange(p2range[0][0] + (maxX - p2range[0][1]), maxX, padding=0)

region.sigRegionChanged.connect(update)

def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

def setRegionCenter(pos):
    minX, maxX = region.getRegion()
    width = maxX - minX
    newRegion = (pos.x() - width / 2, pos.x() + width / 2)
    region.setRegion(newRegion)


p1.sigRangeChanged.connect(updateRegion)
p2.getViewBox().sigMouseClick.connect(setRegionCenter)

region.setRegion([1800, 2000])

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
#p1.addItem(vLine, ignoreBounds=True)
#p1.addItem(hLine, ignoreBounds=True)


vb = p1.vb

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(np.round(mousePoint.x()))
        if index > 0 and index < len(data):
            label.setText("<span style='font-size: 12pt'>Frequency=%0.2f, "
                          "  <span style='color: magenta'>Intensity=%0.2f</span>"
                          % (mousePoint.x(), data[index]))
        #vLine.setPos(mousePoint.x())
        #hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)

