# python 2,3

import sys
import math
import bisect
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

from peak_tools import find_peaks, baselevel_and_noiselevel

from matplotlib import rc
rc('font',**{'family':'serif', 'size' : 10})
rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

class Trans:
    def __init__(self, E, nu, g, J, K):
        self.E  = E
        self.nu = nu
        self.g  = g
        self.J  = J
        self.K  = K
        self.I  = None
        self.Y  = None
        self.A  = None
        self.v  = None
        

def residual(theta, xxx, y_exp):
    y_calc, _ = model_function(xxx, y_exp, theta)
    return y_exp - y_calc
    

def transitions():
    
    # from CDMS for CH3CN;v=0;E  
    transitions1 = [
        Trans(E=930.2925,nu=330.0023439,g=74,J=18,K=13),
        Trans(E=693.2709,nu=330.3047887,g=74,J=18,K=11),
        Trans(E=589.4403,nu=330.4374137,g=74,J=18,K=10),
        Trans(E=411.2546,nu=330.6652067,g=74,J=18,K=8),
        Trans(E=336.9392,nu=330.7602839,g=74,J=18,K=7),
        Trans(E=217.9471,nu=330.9126084,g=74,J=18,K=5),
        Trans(E=173.2971,nu=330.9697941,g=74,J=18,K=4),
        Trans(E=113.7402,nu=331.0460962,g=74,J=18,K=2),
        Trans(E=98.8467,nu=331.0651815,g=74,J=18,K=1),
        Trans(E=93.8818,nu=331.0715436,g=74,J=18,K=0)
    ]
    
    # from CDMS for CH3CN;v=0;A   
    transitions2 = [
        Trans(E=806.8966,nu=330.1597465,g=148,J=18,K=12),
        Trans(E=495.4279,nu=330.5575689,g=148,J=18,K=9),
        Trans(E=272.4986,nu=330.8427622,g=148,J=18,K=6),
        Trans(E=138.5589,nu=331.0142959,g=148,J=18,K=3)
    ]
    
    # from CDMS for CH3CN;v8=1;E   
    transitions3 = [
        Trans(E=693.0519,nu=331.7414752,g=74,J=18,K=6),
        Trans(E=702.5147,nu=331.7687027,g=74,J=18,K=8),
        Trans(E=575.4901,nu=331.8940692,g=74,J=18,K=4),
        Trans(E=582.2570,nu=331.9224950,g=74,J=18,K=6),
        Trans(E=531.5462,nu=331.9503368,g=74,J=18,K=3),
        Trans(E=536.9629,nu=331.9812571,g=74,J=18,K=5),
        Trans(E=476.0960,nu=332.0672246,g=74,J=18,K=3),
        Trans(E=460.5389,nu=332.1076542,g=74,J=18,K=2),
        Trans(E=459.1725,nu=332.0158179,g=74,J=18,K=0)
    ]
    
    transitions4 = [
        Trans(E=454.8036,nu=331.7485182,g=148,J=18,K=1),
        Trans(E=473.3817,nu=332.0178557,g=148,J=18,K=1),
        Trans(E=850.0866,nu=331.5371755,g=148,J=18,K=8),
        Trans(E=629.3294,nu=331.8243297,g=148,J=18,K=5),
        Trans(E=637.4451,nu=331.8517422,g=148,J=18,K=7),
        Trans(E=497.5076,nu=331.9923536,g=148,J=18,K=2),
        Trans(E=501.5731,nu=332.0287582,g=148,J=18,K=4) 
    ]
    
    return [transitions1, transitions2]


def model_function(xxx, y_exp, theta):
    
    kB_wn  = 0.69503477e+0   # cm-1/K
    kB_MHz = 2.08366121e+4   # MHz /K
    
    trans_sets = transitions()
    y_calc     = np.zeros(y_exp.shape) 
    
    lstC = theta[:-1]
    T    = theta[-1]
    
    for trans, C in zip(trans_sets, lstC):
        for t in trans:

            mufactor = float(t.J**2 - t.K**2) / float(t.J * (2*t.J + 1))
           
            A_B_B = 158099.0 * 9198.8992 * 9198.8992
            partition = 5.34e+6 / 3 * math.sqrt(T**3 / A_B_B)
           
            t.A = C * mufactor / partition
           
            tau = t.A * t.g * math.exp( -t.E / (kB_wn * T) )
  
            #t.I = A * ( 1.0 - math.exp(-tau) )
            t.I = tau
    
            # etwas intelligentere Zuordnung
            index = bisect.bisect_left(xxx, t.nu)  
            eps = 1e-6
            
            if y_exp[index] > eps:
                pass
            elif y_exp[index + 1] > eps:
                index = index + 1
            elif y_exp[index - 1] > eps:
                index = index - 1
            else:
                t.I = 0.0
            
            y_calc[index] = t.I
            t.Y = y_exp[index]
    
    return y_calc, trans_sets
    

def peakfinder(data):
    
    base_l, noise_l = baselevel_and_noiselevel(data[:, 1], nbins=4000)
    
    peaks_all, _ = find_peaks(data, thresholds = [noise_l])
    
    data_simple = np.zeros(len(data[:, 1]))
    
    for i, peak in enumerate(peaks_all):
        x1 = peak
        while data[x1, 1] > data[peak, 1] / 2: x1 = x1 + 1
        x2 = peak
        while data[x2, 1] > data[peak, 1] / 2: x2 = x2 - 1
        
        if (data[x1, 0] - data[x2, 0]) < 0:
            continue
            
        data_simple[peak] = data[peak, 1] * (data[x1, 0] - data[x2, 0])
    
    return data_simple


def fit(filename):
    
    # Pi*Daumen initial params
    C = 1
    T = 300   
    theta0 = (C, C, C, C, T)

    data = np.loadtxt(filename)
    
    xxx  = data[:, 0]
    needs_peakfinder = True
    
    if not needs_peakfinder:
        y_exp = data[:, 1]
    else:
        y_exp = peakfinder(data)
    
    theta_optimal = optimize.leastsq(residual, theta0, args=(xxx, y_exp))

    y_calc, trans = model_function(xxx, y_exp, theta_optimal[0])   
    diff = y_exp - y_calc
    T = theta_optimal[0][4]

    all_trans = [t for t_list in trans for t in t_list]
    all_trans.sort(key=lambda t: t.E)
    

    return xxx, y_exp, y_calc, T, all_trans
    

if __name__ == "__main__":
    folder = "./"
    suffixes = ["RT", "340K"]

    f2 = plt.figure()
    ax1 = f2.add_subplot(111)
    ax1.set_xlabel(r"Lower state energy [cm-1]")
    ax1.set_ylabel(r"$I / (A * g_{upper}$) [integrated]")
    ax1.tick_params(labelsize=14, direction = 'in')
    ax1.set_yscale('log')
    
    for suffix in suffixes:
        
        filename = folder + suffix + '_norm_mean_spec.txt'
        xxx, y_exp, y_calc, T, all_trans = fit(filename)
        
        print ("T  = " + str(T))
        
        xxx_t    = [t.E for t in all_trans]
        y_calc_t = [t.I / (t.A * t.g) for t in all_trans]
        y_exp_t  = [t.Y / (t.A * t.g) for t in all_trans]
        K_vals   = [t.K for t in all_trans]

        ax1.plot(xxx_t, y_exp_t,  color = 'grey', lw=1)
        
        if suffix == "RT":
            ax1.plot(xxx_t, y_calc_t, color = 'b', lw=1, label = (r"Fit: T = %i K" %round(T,0)))
        else:
            ax1.plot(xxx_t, y_calc_t, color = 'g', lw=1, label = (r"Fit: T = %i K" %round(T,0)))

    ax1.legend()
    filename = folder + 'Fit/boltzmann_diagram_both2.pdf' 
    plt.savefig(filename, papertype = 'a4', orientation = 'landscape')
    plt.close()
    
    sys.exit()
    
    
    print (theta_optimal[0])
    print ("T  = " + str(T))
    
    filename = folder + 'Fit/fitted_%s_fit.txt' % suffix
    np.savetxt(filename, np.stack([xxx, y_exp, y_calc, diff]).T, header = "Frequencies		Intensities(obs)		Intensities(calc)		Difference(obs-calc=)")
    
    #sys.exit()

    f2 = plt.figure()
    ax1 = f2.add_subplot(111)
    ax1.set_xlabel(r"Lower state energy [cm-1]")
    ax1.set_ylabel(r"$I / (A * g_{upper}$) [integrated]")
    ax1.tick_params(labelsize=14, direction = 'in')
    ax1.set_yscale('log')
    ax1.plot(xxx_t, y_exp_t,  color = 'k', lw=1,   label = r"Messwerte")
    ax1.plot(xxx_t, y_calc_t, color = 'r', lw=0.7, label = (r"Fit: T = %i K" %round(T,0)))
    ax1.legend()
    
    for K, x, y in zip(K_vals, xxx_t, y_exp_t):
        ax1.annotate(str(K), (x, y))
    
    filename = folder + 'Fit/boltzmann_diagram_%s.pdf' % suffix
    plt.savefig(filename, papertype = 'a4', orientation = 'landscape')
    plt.close()

    
    f1 = plt.figure()
    ax1 = f1.add_subplot(111)
    ax1.set_xlabel(r"Transition frequency [GHz]")
    ax1.set_ylabel(r"$I$ [integrated]")
    ax1.tick_params(labelsize=14, direction = 'in')
    ax1.plot(xxx, y_exp, color = 'k', lw=1,  label = r"Messwerte")
    ax1.plot(xxx, y_calc, color = 'r', lw=0.7, label = (r"Fit: T = %i K" %round(T,0)))
    ax1.legend()
    filename = folder + 'Fit/fitted_spec_Fit_%s.pdf' % suffix
    plt.savefig(filename, papertype = 'a4', orientation = 'landscape')
    plt.close()

    
    #f2 = plt.figure()
    #ax1 = f2.add_subplot(111)
    #ax1.set_xlabel(r"Frequency / GHz")
    #ax1.set_ylabel(r"$I_{obs}-I_{calc}$")
    #ax1.tick_params(labelsize=12, direction = 'in')
    #ax1.plot(xxx, diff, color = 'k', lw=1, label = (r"T = %i K" %round(T,0)))
    #ax1.legend()
    #filename = folder + 'Fit/fitted_obs-calc_%s.pdf' % suffix
    #plt.savefig(filename)
    #plt.close()


