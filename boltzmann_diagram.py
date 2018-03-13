# python 2,3

import numpy as np
import matplotlib.pyplot as plt

from bisect import bisect_left
from lmfit.models import ExponentialModel, LinearModel

from matplotlib import rc
rc('font',**{'family':'serif', 'size' : 10})
rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

class Trans:
    def __init__(self, E, nu, g, J, K, A=None):
        self.E  = E
        self.nu = nu
        self.g  = g
        self.J  = J
        self.K  = K
        self.A  = A
        self.Y  = None    # exp intensity
        

def transitions():
    
    # from CDMS for CH3CN;v=0;E  
    transitions1 = [
        Trans(E=930.2925,nu=330.0023439,g=74,J=18,K=13,A=0.0014973),
        Trans(E=693.2709,nu=330.3047887,g=74,J=18,K=11,A=0.0019663),
        Trans(E=589.4403,nu=330.4374137,g=74,J=18,K=10,A=0.0021725),
        Trans(E=411.2546,nu=330.6652067,g=74,J=18,K=8,A=0.0025267),
        Trans(E=336.9392,nu=330.7602839,g=74,J=18,K=7,A=0.0025267),
        Trans(E=217.9471,nu=330.9126084,g=74,J=18,K=5,A=0.0029126),
        Trans(E=173.2971,nu=330.9697941,g=74,J=18,K=4,A=0.0029126),
        Trans(E=113.7402,nu=331.0460962,g=74,J=18,K=2,A=0.0031212),
        Trans(E=98.8467,nu=331.0651815,g=74,J=18,K=1,A=0.0031508),
    ]
    
    # from CDMS for CH3CN;v=0;A   
    transitions2 = [
        Trans(E=806.8966,nu=330.1597465,g=148,J=18,K=12,A=0.0017414),
        Trans(E=495.4279,nu=330.5575689,g=148,J=18,K=9,A=0.0023595),
        Trans(E=272.4986,nu=330.8427622,g=148,J=18,K=6,A=0.0028035),
        Trans(E=138.5589,nu=331.0142959,g=148,J=18,K=3,A=0.0030716),
        Trans(E=93.8818,nu=331.0715436,g=74,J=18,K=0,A=0.0031607)
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
    
    return transitions1 + transitions2



def assign(expdata, trans):
    
    xxx  = expdata[:, 0]
    y_exp = expdata[:, 1]  

    eps = 1e-6
    new_trans = []
    for t in trans:

        index = bisect_left(xxx, t.nu)  
        
        if y_exp[index] > eps:
            pass
        elif y_exp[index + 1] > eps:
            index = index + 1
        elif y_exp[index - 1] > eps:
            index = index - 1
        else:
            print('Not assigned: ' + str(t.nu))
            continue
        
        t.Y = y_exp[index]
        new_trans.append(t)
    
    return new_trans


def fit(filename):
    
    kB_wn  = 0.69503477   # cm-1/K  
    
    data = np.loadtxt(filename)
    
    trans = transitions()
    trans = assign(data, trans)
    trans = sorted(trans, key=lambda t: t.E)

    xxx    = [t.E               for t in trans]
    y_exp  = [t.Y / (t.A * t.g) for t in trans]
    y_exp = list(np.log(y_exp))
    
    model = LinearModel()
    pars = model.make_params(intercept=5.0, slope=-1.0/(kB_wn*300))
   
    out = model.fit(y_exp, pars, x=xxx)
  
    y_calc = out.best_fit
    T = - 1 / (kB_wn * out.params['slope'])
    
    return xxx, y_exp, y_calc, T, trans
    

if __name__ == "__main__":
    folder = "/home/borisov/projects/work/emission/advanced/"
    suffixes = ["RT", "340K"]

    f2 = plt.figure()
    ax1 = f2.add_subplot(111)
    ax1.set_xlabel(r"Lower state energy [cm-1]")
    ax1.set_ylabel(r"$I / (A * g_{upper}$) [integrated]")
    ax1.tick_params(labelsize=14, direction = 'in')
    ax1.set_yscale('log')
    
    for suffix in suffixes:
        
        filename = folder + suffix + '_norm_peaks.txt'
        xxx, y_exp, y_calc, T, trans = fit(filename)
        
        y_exp = list(np.exp(y_exp))
        y_calc = list(np.exp(y_calc))
        
        print ("T  = " + str(T))
        
        ax1.plot(xxx, y_exp,  color = 'grey', lw=1)
        
        if suffix == "RT":
            ax1.plot(xxx, y_calc, color = 'b', lw=1, label = (r"Fit: T = %i K" %round(T,0)))
        else:
            ax1.plot(xxx, y_calc, color = 'g', lw=1, label = (r"Fit: T = %i K" %round(T,0)))

    ax1.legend()
    filename = folder + 'Fit/boltzmann_diagram_both4.pdf' 
    plt.savefig(filename, papertype = 'a4', orientation = 'landscape')
    plt.close()
    
