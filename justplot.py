#!/usr/bin/python
# Just a simple plot of spectra

import sys;
import numpy as np;
import matplotlib.pyplot as pl;

# input filenames
if len(sys.argv) < 2: 
	name_file = raw_input("Enter filename, please: ");
else:
	name_file = sys.argv[1];

data = np.loadtxt(name_file); 

x = data[:,0];
y = data[:,1];
#y[y < 0] = 0;

pl.plot(x, y);
pl.show();
