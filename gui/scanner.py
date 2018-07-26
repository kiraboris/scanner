
import numpy as np
from .pyqtgraph.Qt import QtGui

from . import pyqtgraph as pg
from . import panoram

app = QtGui.QApplication([])
win = QtGui.QWindow()
win.show()
win.setTitle('scanner')

pan = panoram.Panoram()
label = pg.LabelItem(justify='right')

#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

pan.plotUpper(data=data, pen="m")
pan.plotLower(data=data, pen="0ff")

pan.region.setRegion([1800, 2000])

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

