# python 
#

import numpy as np

class Ranges:
    
    def __init__(self, arrays=[]):
        """'arrays': list of numpy arrays"""

        self.__arrs = arrays
    
    def max_height(self, dim=None):
        
        if dim is None:
            return max([max(a) - min(a) for a in self.__arrs])
        else:
            return max([max(a[:, dim]) - min(a[:, dim]) for a in self.__arrs])
            
    def nslices(self, step, span, dim=None):
        
        nbins = 0
        for a in self.__arrs:
            left = 0
            right = 0

            if dim is None:
                xa = a    
            else:
                xa = a[:, dim]
            
            nbins += ((xa[-1]-span/2) - (xa[0]+span/2)) / step
            
        return int(nbins)

    def slices(self, step, span, dim=None):
        """'span': size of slice,
           'step': offset of each next slice from begin of previous one"""
        
       
        for a in self.__arrs:
            left = 0
            right = 0
            
            if dim is None:
                xa = a    
            else:
                xa = a[:, dim]
            
            bins = np.arange(xa[0]+span/2, xa[-1]-span/2, step)

            for x in bins:
                while xa[left]  <= x - span/2.0: left  = left  + 1
                while xa[right] <  x + span/2.0: right = right + 1
                
                if dim is None:
                    yield a[left:right]
                else:
                    yield a[left:right, :]

