#!/usr/bin/env python

import numpy as np
import scipy.sparse.linalg
import matplotlib.pyplot as plt

from scipy.sparse import csc_matrix, spdiags
from scipy.interpolate import splev, splrep

# Constants
STR_SOURCE_FILE = "Methyl_Cyanide_10_new.txt"
STR_TARGET_FILE = "Methyl_cyanide_10_new_baseline.txt"



#===============================================================================
# 'Asymmetric Least Squares Smoothing' by P. Eilers and H. Boelens
#===============================================================================

def baseline_als(y, lam, p, niter=15):
    L = len(y)
    D = csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in xrange(niter):
        W = spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = scipy.sparse.linalg.spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z



#===============================================================================
# Main
#===============================================================================

# Read data
data = np.loadtxt(STR_SOURCE_FILE)

# Reverse arrays
freq = data[:,0]
ampl = data[:,2]
freq_usb = data[::-1,1]
ampl_usb = data[::-1,2]

# Fit data
base_fit = baseline_als(ampl[::4], 2.0e02, .0025, niter=20)
tck = splrep(freq[::4], base_fit)

fit_all = splev(freq, tck)

# Plot fitted data
plt.plot(freq, fit_all)
plt.plot(freq, ampl)
plt.plot(freq, ampl - fit_all)

plt.plot(freq_usb, fit_all[::-1])
plt.plot(freq_usb, ampl_usb)
plt.plot(freq_usb, ampl_usb - fit_all[::-1])

plt.show()

# Save fitted data
np.savetxt(save_name + '.txt', np.c_[freq, freq_usb[::-1], ampl, ampl-fit_all])


