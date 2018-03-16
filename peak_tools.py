"""
python 2.7 / 3.4

find_peaks(data, thresholds, minimal_linewidth=2)
    Finds peaks indices in each dataset, finds common peaks.
    
    data: 
        numpy array of N+1 columns (x, y_1, ..., y_N)
    thresholds: 
        array-like of length N
    minimal_linewidth:
        integer amount of datapoints (channels) 
    returns: 
        tuple(peaks_all, peaks_common) 

downsample(data, ntimes=2)
    Divides sampling rate by ntimes, take average over adjancent points.
    
    data: 
        numpy array of N+1 columns (x, y_1, ..., y_N) 
        with shape[0] == LEN
    returns:
        numpy array of N+1 columns (x, y_1, ..., y_N) 
        with shape[0] == LEN / ntimes


delete_peak(spec, freq)
    Sets Y-values for given X-values to zero (removes spikes in spectrum).
    
    spec: 
        numpy array of 2 columns (x, y)
    freq:
        list or scalar: X-values to remove Y at
        

"""

import numpy as np
import peakutils
import collections

# deletes peak at freq (for better baseline-fit)
def delete_peak(spec, freq, axis=None, eps=1e-15):

    if isinstance(freq, collections.Iterable):
        freq_list = freq
    else:
        freq_list = list((freq,))    
    for i in range(0, len(spec[:,0])):

        flagBlanck = False
        for x in freq_list:
            if isinstance(x, tuple):
                if spec[i,0] >= x[0] and spec[i,0] <= x[1]:
                    flagBlanck = True
            else:
                if abs(spec[i,0] - x) < eps:
                    flagBlanck = True
            
        if flagBlanck:
            if not axis:
                spec[i, 1:] = 0
            else:
                spec[i, axis] = 0
            
    return spec

    
# determines base level (avg of noise)
#  requires flat baseline
def baselevel_and_noiselevel(data, nbins=2000, lpercentile=.001):
  
   hist, slices  = np.histogram(data, bins=nbins) 
   bl = (slices[np.argmax(hist)] + slices[np.argmax(hist) + 1]) / 2
   nl = 2 * bl - np.percentile(data, lpercentile)
        
   return bl, nl
       
    
def downsample(data, ntimes=2):
        
    new_size = int(data.shape[0] / ntimes)
    end =  ntimes * new_size
    
    data_out = np.zeros([new_size, data.shape[1]]) 
    
    for i, data_slice in enumerate(data.T):
        data_out[:,i] = np.mean(data_slice[:end].reshape(-1, ntimes), axis=1)
        
    return data_out
    

def find_peaks(data, thresholds, minimal_linewidth=2):
    
    # == settings ==
    xxx = data[:, 0]            # 0th dataset are X values
    delta = minimal_linewidth*3   # different datasets have slightly shifted peaks
    # ==============

    # determine minimal linehights 
    noise_levels = thresholds
    minimal_lineheights = []
    for d, nl in zip(data[:, 1:].T, noise_levels):
        y_max = max(abs(d))
        minimal_lineheights.append(nl / y_max)

    print ("--peak finder--")
    print ("Assumed noise levels [K]: " + 
           ", ".join(["%0.2f" % x for x in noise_levels]))
    print ("Assumed least peakwidth :", minimal_linewidth, 'channels')

    # find peaks
    peak_index_sets = []
    for (d, t) in zip(data[:, 1:].transpose(), minimal_lineheights): 
        peak_index_sets.append(set(peakutils.indexes(d, thres = t, 
                            min_dist = minimal_linewidth)))
                                
    peak_indexes_union = reduce(set.union, peak_index_sets)
    
    if len(data[:, 1:].transpose()) == 1:  # only one Y dataset
        peak_indexes_common = peak_indexes_union
        return (list(peak_indexes_union), list(peak_indexes_common))
    
    # find intersection of peak list, accounting for linewidth
    peak_indexes_common =  set()
  
    if False:     # old habit - take all peak indexes for "broad" peaks 
                  # not optimal algorithm, looks through same span many times
        for peak_pos in peak_indexes_union:
            flag = True
            for peakset in peak_index_sets:
                span = [peak_pos + i for i in range(-delta, delta)]
                flag = flag & any([x in peakset for x in span])
            if flag:
                peak_indexes_common.add(peak_pos)
    else:     # take one "most peaky" peak index for "broad" peaks
              #   by sum(peak_intensities) -> max
        for peak_pos in peak_index_sets[0]:
            blended_peak_pos = []
            flag = True
            for i, peakset in enumerate(peak_index_sets):
                span = [peak_pos + i for i in range(-delta, delta)]
                local_blended_peak_pos = [x for x in span if x in peakset]
                if local_blended_peak_pos:
                    blended_peak_pos.extend(local_blended_peak_pos)
                else:
                    flag = False
            if flag:
                real_peak_pos = sorted(blended_peak_pos, 
                                       key=lambda x: sum(data[x, 1:]),
                                       reverse=True)[0]
                peak_indexes_common.add(real_peak_pos)
            
    
    print ("Found %d peaks in total." % len(peak_indexes_union))
    print ("Found %d common peaks." % len(peak_indexes_common))
    print ("")
    
    return (list(peak_indexes_union), list(peak_indexes_common))
    
    
