# python 2.7
#
# classes: SymmRotor
#
import math

class SymmRotorNK:
    """symmetric rotor with N (aka l) and K""" 
    
    def __remove_minus_inplace(self, dict_quanta):
        """docstring"""
        
        for key in dict_quanta:
            dict_quanta[key] = abs(dict_quanta[key])
    
    
    def __spin_symm(self, entry):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if hasattr(entry, "dict_quanta"):
            quanta = entry.dict_quanta
        elif hasattr(entry, "q_upper"):
            quanta = entry.q_upper
        
        if (quanta['N'] + quanta['K']) % 3 == 0:
            return 'E'
        else:
            return 'A'
    

    def __merge(self, blends):
        """docstring"""
        
        result = blends[0]
        
        if hasattr(result, "flt_log_I"):
            I_bl = map(lambda x: 10 ** x.flt_log_I, blends)
            g_bl = map(lambda x: x.int_g if 10 ** x.flt_log_I == max(I_bl) else 0, blends)
            result.flt_log_I = math.log10(sum(I_bl))
            result.int_g     = sum(g_bl);
        else:
            g_bl = map(lambda x: x.int_g, blends)
            result.int_g = sum(g_bl)        
        
        return result
    
    
    def strip_parity(self, entries):
        """in-place"""
        blends = []
        for entry in entries:
            if hasattr(entry, "dict_quanta"):
                self.__remove_minus_inplace(entry.dict_quanta)
                
            elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
                self.__remove_minus_inplace(entry.q_upper)
                self.__remove_minus_inplace(entry.q_lower)
    
    
    def merge_blends(self, entries):
        """in-place"""
        result = []
        blends = []
        for i in range(1, len(entries) + 1):
            
            prev = entries[i - 1]
            
            if(i < len(entries)):
                curr = entries[i]

                if(curr == prev and self.__spin_symm(curr) != "A"):
                    blends.append(prev)
                else:
                    if(blends):
                        blends.append(prev)
                        result.append(self.__merge(blends))
                        blends = []
                    else:
                        result.append(prev)
        
        entries[:] = result  # deep copy implicitely frees unused duplicates
