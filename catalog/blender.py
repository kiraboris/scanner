# python 2.7
#
# classes: Blender
#
from abc import ABC

class Blender(ABC):
    """Delegate type that merges states and transitions.
       Its functions are called from a quantum model 
       and recieve already selected "equivalent" objects, where
       "Equivalence" is defined by the parent quantum model."""
    
    @abstractmethod
    def merge_lines(self, lst_blends):
        pass
        
    @abstractmethod
    def merge_state(self, lst_blends):
        pass

        
class DefaultBlender(Blender):
    """delegate type that work with both states and transitions"""
    
    def merge_lines(self, blends):
        """docstring"""
        
        I_bl = map(lambda x: 10 ** x.flt_log_I, blends)
        g_bl = map(lambda x: x.int_g if 10 ** x.intensity == max(I_bl) else 0, blends)
        
        result           = blends[0]
        result.flt_log_I = math.log10(sum(I_bl))
        result.int_g     = sum(g_bl);
        
        return result
    
    
    def merge_states(self, blends):
        """docstring"""
        
        g_bl = map(lambda x: x.int_g, blends)
        
        result       = blends[0]
        result.int_g = sum(g_bl);
        
        return result