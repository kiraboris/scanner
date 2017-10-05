import pylab;
import numpy;
import peakutils;

x=numpy.linspace(0,20,1000);
y=numpy.sin(x);

indexes = peakutils.indexes(y, thres=0.02*max(y), min_dist=100);

pylab.plot(x,y, label='line');
pylab.plot(x[indexes], y[indexes], 'bo', label='peaks');
pylab.legend();
pylab.show();


