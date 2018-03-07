# python 
#

import numpy as np
import pint

class DIM:
    """np.array dimensions"""
    X = 0
    Y = 1


class Units:
    
    @staticmethod
    def prefixes():
        return [
            'yocto- = 1e-24 = y-',
            'zepto- = 1e-21 = z-',
            'atto- =  1e-18 = a-',
            'femto- = 1e-15 = f-',
            'pico- =  1e-12 = p-',
            'nano- =  1e-9  = n-',
            'micro- = 1e-6  = u- = µ-',
            'milli- = 1e-3  = m-',
            'centi- = 1e-2  = c-',
            'deci- =  1e-1  = d-',
            'deca- =  1e+1  = da- = deka',
            'hecto- = 1e2   = h-',
            'kilo- =  1e3   = k-',
            'mega- =  1e6   = M-',
            'giga- =  1e9   = G-',
            'tera- =  1e12  = T-',
            'peta- =  1e15  = P-',
            'exa- =   1e18  = E-',
            'zetta- = 1e21  = Z-',
            'yotta- = 1e24  = Y-'
        ]
    
    @staticmethod
    def spec_units():
        lst_units = ([
            'second = [time] = s',
            'hertz = 1 / s = Hz',
            'meter = s / 299792458 = m',
            'wavenumber = 1 / cm = wn',
        ] 
        + Units.prefixes())
        
        units = pint.UnitRegistry(None)
        units.load_definitions(lst_units)
        
        return units


class Ranges:
    
    def __init__(self, arrays=[]):
        """'arrays': list of numpy arrays"""

        self.__arrs = arrays
    
    def height(self, dim=None):
        
        if dim is None:
            return max([np.max(a) - np.min(a) for a in self.__arrs])
        else:
            return max([np.max(a[:, dim]) - np.min(a[:, dim]) 
                for a in self.__arrs])
            
    def nslices(self, step, span, nmipmap=0, dim=None):
        
        nbins = 0
        for a in self.__arrs:
            left = 0
            right = 0

            if dim is None:
                xa = a    
            else:
                xa = a[:, dim]
            
            nbins += (((xa[-1]-span/2) - (xa[0]+span/2)) / step) * (nmipmap + 1)
            
        return int(nbins)

    def slices(self, step, span, nmipmap=0, dim=None):
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
                
                mleft = left
                mright = right
                for n in range(0, nmipmap + 1):
                
                    if dim is None:
                        yield a[mleft:mright]
                    else:
                        yield a[mleft:mright, :]
                    
                    mleft  += int((mright - mleft) / 4)
                    mright -= int((mright - mleft) / 4)
                    

