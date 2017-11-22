# python 3
#
# classes: SymmRotor
#

import math
from multidict import MultiDict
from functools import partial as bind

from basic_structs import Line, State


def custom_quanta_transform(entries, func_transform):
    """docstring"""

    for entry in entries:
        if hasattr(entry, "q"):
            entry.q = func_transform(entry.q)
            
        elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
            entry.q_upper = func_transform(entry.q_upper)
            entry.q_lower = func_transform(entry.q_lower)



class SymmRotor:
    """symmetric rotor with N (aka J), K and possibly v, l""" 
    
    def __pv2vl(self, quanta, mapper):
        """docstring"""
        
        quanta['v'], quanta['l'] = mapper[quanta.get('v', 0)]
    
    
    def __vl2pv(self, quanta, mapper):
        """docstring"""

        quanta['v'] = mapper.inv[(quanta['v'], quanta.['l'])]
    
    
    def extract_vl_from_pseudo_v(entries, mapper):
        """docstring"""
        
        custom_quanta_transform(entries, bind(self.__pv2vl, mapper=mapper))
        
        
    def compress_vl_to_pseudo_v(entries, mapper):
        """docstring"""
       
        custom_quanta_transform(entries, bind(self.__vl2pv, mapper=mapper))
    
    
    def __spin_symm(self, quanta):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if (quanta['K'] - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'
    
    
    def __merge(self, blends):
        """docstring"""
        
        result = blends[0]
        
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
    
    
    def __build_dict(self, entries):
        """docstring"""
        
        result = MultiDict()
        for e in entries:
            result[e.qid()] = e
            
        return result
        
    
    # assuption: entries can be partitioned into mergable classes
    def fix_blends(self, entries):
        
        dict_entries = self.__build_dict(entries)
        
        
        
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
