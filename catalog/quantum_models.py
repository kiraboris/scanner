# python 2.7
#
# classes: SymmRotor
#

import copy
import math

from pickett_io import Line, State, CatConverter

class BasicRotor:
    """basic operations"""
    
    def custom_quanta_transform(self, entries, func_transform):
        for entry in entries:
            if hasattr(entry, "quanta"):
                func_transform(entry.quanta)
                
            elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
                func_transform(entry.q_upper)
                func_transform(entry.q_lower)
        


class SymmRotor(BasicRotor):
    """symmetric rotor with N (aka J), K and possibly v, l""" 
    
    
    def spin_symm(self, quanta):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if (quanta['K'] - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'
    
    
    def __merge(self, blends):
        """docstring"""
        
        result = copy.deepcopy(blends[0])
        
        if isinstance(result, Line):
            
            if(self.spin_symm(result.q_upper) == "A"):
                result.q_lower['K'] = -(result.q_upper['K'])
            
            I_bl = map(lambda x: 10 ** x.log_I, blends)
            g_bl = map(lambda x: x.g, blends)
            
            result.log_I = math.log10(sum(I_bl))
            
            result.g = 0
            for (I, g) in zip(I_bl, g_bl):
                if( I == max(I_bl) ):
                    result.g += g
        
        elif isinstance(result, State): 
            
            g_bl = map(lambda x: x.g, blends)
            result.g = sum(g_bl)
            
        else:
            raise Exception("Neigher line nor state")
        
        return result
    
    
    def __are_mergable(self, first, second):
         """docstring"""
         
         if( first is None or second is None ):
             return False
             
         elif( vars(first).keys() == vars(second).keys() ):
            if isinstance(first, State):
                qf = first.quanta.copy()
                qs = second.quanta.copy()
                
                return(qf == qs )
                
            elif isinstance(first, Line):
                qfu = first.q_upper.copy() 
                qfl = first.q_lower.copy()
                qsu = second.q_upper.copy()
                qsl = second.q_lower.copy()
                
                qfl['K'] = abs(qfl['K'])
                qsl['K'] = abs(qsl['K'])
                
                return(qfu == qsu and qfl == qsl)
            
            else:
                raise Exception("Neigher line nor state")
    
    
    # assuption: entries can be partitioned into mergable classes
    def merge_blends(self, entries, max_blends = 8):

        MAX_BLENDS = max_blends
        
        result = []
        blends = []
        
        i = 0
        ignore_i = set()
        for i in range(0, len(entries)):
            
            if i in ignore_i:
                continue
            
            for j in range(1, min(MAX_BLENDS, len(entries) - i)):
                if(self.__are_mergable(entries[i], entries[i+j])):
                    blends.append(entries[i+j])
                    ignore_i.add(i+j)

            if(blends):
                blends.append(entries[i])
                result.append(self.__merge(blends))
                blends = []
            else:
                result.append(entries[i])
       
        
        return result
