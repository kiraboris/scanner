# python 2.7
#
# classes: SpeciesEntry
#

from pickett_io import CatConverter, EgyConverter

class SpeciesEntry:
    
    def __init__(self):
        """docstring"""
        
        self.lines  = []
        self.states = []
        
        self.int_quanta_fmt = None
        
        
    def load_cat(self, str_filename):
        """Read from .cat"""
        
        with open(str_filename, 'r') as f:
            self._lst_lines  = []
            
            for str_line in f:
                obj = CatConverter.str2line(str_line)
                self._lst_lines.append(obj)
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
            
            for str_state in f:
                obj = EgyConverter.str2state(str_state, self.int_quanta_fmt)
                self._lst_states.append(obj)
                 
    
    def save_cat(self, str_filename):
        """docstring"""
        
        with open(str_filename, 'w') as f:
            for obj_line in self._lst_lines:
                textline = CatConverter.line2str(obj_line)
                f.write(textline)
                
                
    def save_egy(self, str_filename):
        """docstring"""
        assert self.int_quanta_fmt
        
        with open(str_filename, 'w') as f:
            for obj_state in self._lst_states:
                textline = EgyConverter.state2str(obj_state, self.int_quanta_fmt)
                f.write(textline)
    
