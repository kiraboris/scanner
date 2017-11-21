# python 2.4
import numpy as np
import peakutils

def main():
    
    # ALL spectra in one file - to obtain, run match.py
    data = np.loadtxt('out.txt')  
    
    peaks_all, peaks_common = find_peaks(data, noise_nsigma=5)
    
    xxx = data[:, 0]
    yyy = np.zeros(len(xxx))
    
    
    # print statistics example (you way want something different)
    print "--statistics--"
    
    cV =  ( np.std(data[peaks_common, 1:], axis=1) /
            np.abs(np.mean(data[peaks_common, 1:], axis=1)) ) 
                           
    print "Coefficients of variance for common peaks:"
    print "  min %0.1f%%" % (min(cV) * 100)
    print "  max %0.1f%%" % (max(cV) * 100)
    print "  avg %0.1f%%" % (np.mean(cV) * 100)
        
    
    # plot example (you may want other plots)
    import matplotlib
    import matplotlib.pyplot as pl
    import matplotlib.gridspec as plgs
    
    my_fontsize = 16

    f1 = pl.figure()
    ax1 = f1.add_subplot(111)
    ax1.set_xlabel("Frequency [GHz]", fontsize=my_fontsize)
    ax1.tick_params(labelsize=my_fontsize-3)

    yyy[peaks_common] =  np.mean(data[peaks_common, 1:], axis=1)
    
    ax1.plot(xxx / 1000, yyy, 'k-', lw = 2)
    ax1.legend(['$\mu_{obs}$'])

    ax1.tick_params(direction = 'in')
    ax1.grid()
    pl.show()
    
    #f1.canvas.draw()  
    #ylabels = [item.get_text() + "%" for item in ax1.get_yticklabels()]
    #ax1.set_yticklabels(ylabels)
    
    
    
    
#   
# Do not edit below!
#
    
def find_peaks(data, noise_nsigma=2):
    # == settings ==
    xxx = data[:, 0]                # 0th dataset are X values
    minimal_linewidth = 2           # a line peak is at least 2 channels wide
    delta = minimal_linewidth * 2   # diffrenet datasets have slightly shifted peaks
    # ==============

    # determine minimal linehights # TODO: find a smarter way
    minimal_lineheights = []
    noise_levels = []
    for d in data[:, 1:].transpose():
        y_std   = np.std(d)
        y_max = max(abs(d))
        thresh = noise_nsigma * y_std
        minimal_lineheights.append(thresh / y_max)
        noise_levels.append(thresh)

    print "--peak finder--"
    print "Assumed noise levels [K]: " + ", ".join(["%0.2f" % x for x in noise_levels])
    print "Assumed least peakwidth :", minimal_linewidth, 'channels'

    # find peaks
    peak_index_sets = []
    for (d, t) in zip(data[:, 1:].transpose(), minimal_lineheights): 
        peak_index_sets.append(set(peakutils.indexes(d, thres = t, 
                            min_dist = minimal_linewidth)))
                                
    peak_indexes = list(reduce(set.union, peak_index_sets))

      # find intersection of peak list, accounting for linewidth
    # 'flatten' broad peaks
    peak_indexes_common =  []
    for peak_pos in peak_indexes:
        flag = True
        for peakset in peak_index_sets:
            span = [peak_pos + i for i in range(-delta, delta)]
            flag = flag & any([x in peakset for x in span])
        if flag:
            peak_indexes_common.append(peak_pos)	
    
    print "Found %d peaks in total." % len(peak_indexes)
    print "Found %d common peaks." % len(peak_indexes_common)
    print ""
    
    return (peak_indexes, peak_indexes_common)
    
    
    
if( __name__ == "__main__" ):
    main()
