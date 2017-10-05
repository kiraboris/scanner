import numpy as np
from scipy.sparse import csc_matrix, spdiags
import scipy.sparse.linalg
from scipy.interpolate import splev, splrep
import matplotlib.pyplot as plt

# load data
filename = '15N_raw'
data = np.loadtxt(filename + '.txt')
# name zum speichern
save_name = filename + '_baseline'
###########################
## setup func for baseline fit
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
###########################
# reverse array
freq = data[:,0]
ampl = data[:,2]
freq_usb = data[::-1,1]
ampl_usb = data[::-1,2]


base_fit = baseline_als(ampl[::4], 2.0e02, .0025, niter=20)
tck = splrep(freq[::4],base_fit)

fit_all = splev(freq, tck)

#Asymmetric Least Squares Smoothing" by P. Eilers and H. Boelens in 2005. The paper is free and you can find it on google.
plt.plot(freq,fit_all)
plt.plot(freq,ampl)
plt.plot(freq,ampl-fit_all)
########
plt.plot(freq_usb,fit_all[::-1])
plt.plot(freq_usb,ampl_usb)
plt.plot(freq_usb,ampl_usb-fit_all[::-1])
plt.show()

# save data

np.savetxt(save_name+'.txt',np.c_[freq,freq_usb[::-1],ampl,ampl-fit_all])
