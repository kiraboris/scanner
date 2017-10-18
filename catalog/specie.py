# python 2.7
#
# classes: Specie
#

from pickett_io import CatConverter, EgyConverter

class Specie:
    """A whole species entry"""
    
    def __init__(self, quantum_model = None):
        """docstring"""
        
        self._lst_lines     = []
        self._lst_states    = []
        self.quantum_model  = quantum_model
        self.int_quanta_fmt = None
        
        
    def merge_blends(self):
        """merges some lines and states with same quantum numbers"""
        try:
            self.quantum_model.merge_blended_lines(self._lst_lines)
            self.quantum_model.merge_blended_states(self._lst_states)
        except:
            pass
        
        
    def load_cat(self, str_filename):
        """Read from .cat"""
        
        with open(str_filename, 'r') as f:
            self._lst_lines  = []
            obj_conv = CatConverter()
            
            for str_line in f:
                self._lst_lines.append(obj_conv.str2line(str_line)
                # FUTURE: also fill _lst_states here (case of no .egy)
                
        if self._lst_lines:
            self.int_quanta_fmt = self._lst_lines[0].state_upper.int_fmt
            
                
                
    def load_egy(self, str_filename):
        """Read from .egy
           (previously load_cat() must be run or int_quanta_fmt manually set)
        """
        assert self.int_quanta_fmt
        
        with open(str_filename, 'r') as f:
            self._lst_states  = []
            obj_conv = EgyConverter()
            
            for str_state in f:
                obj = obj_conv.str2state(str_state, self.int_quanta_fmt)
                self._lst_states.append(obj)
                 
    
    def save_cat(self, str_filename):
        """docstring"""
        
        with open(str_filename, 'w') as f:
            obj_conv = CatConverter()
            for obj_line in self._lst_lines:
                f.write(obj_conv.line2str(obj_line))
                
                
    def save_egy(self, str_filename):
        """docstring"""
        assert self.int_quanta_fmt
        
        with open(str_filename, 'w') as f:
            obj_conv = EgyConverter()
            for obj_state in self._lst_states:
                f.write(obj_conv.state2str(obj_state, self.int_quanta_fmt))
    
