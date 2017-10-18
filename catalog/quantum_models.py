# python 2.7
#
# classes: QuantaInterpreterBase, SymmRotorNK
#

from abc import ABS

#from basic_structs import State, Line

class IQuantumModel(ABC):
    """interface of delegate types that work with states and lines"""
    
    @abstractmethod
    def merge_blended_lines(self, lst_lines):
        """in-place merge"""
        pass
    
    @abstractmethod
    def merge_blended_states(self, lst_states):
        """in-place merge"""
        pass



class SymmRotor(IQuantumModel):
    """symmetric rotor with N (aka l) and K""" 
    
    def __spin_symm(self, state):
        """get spin-statistical symmetry irr.rep. of state"""
         
        if (state.dict_quanta['N'] + state.dict_quanta['K']) % 3 == 0:
            return 'E'
        else:
            return 'A'
    
    
    def merge_blended_lines(self, lst_lines):
        """in-place merge"""
        pass
    
    
    def merge_blended_states(self, lst_states):
        """in-place merge"""
        pass
