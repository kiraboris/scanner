# python 2.7
#
# classes: Specie
#

from collections import defaultdict

from pickett_io import CatConverter, EgyConverter

class Specie:
    """A whole species entry"""
    
    def __init__(self):
        """docstring"""
        
        self.__dict_q_to_line     = defaultdict(Line)
        self.__dict_q_to_state    = defaultdict(State)
        self.__bol_respect_parity = True
        
        
    def load_cat(self, str_filename):
        """Read from .cat, merge duplicates (quanta considered unique)"""
        
        with open(str_filename, 'r') as f:
            obj_parser = CatConverter(self.__bol_respect_parity)
            
            for str_line in f:
                str_u = obj_parser.quanta_upper(str_line)
                str_l = obj_parser.quanta_lower(str_line)
                
                obj_line = self.__dict_upper_to_line[str_u]
                obj_parser.update_line(obj_line, str_line)
                self.__dict_lower_to_line[str_l] = obj_line
                
                
    def load_egy(self, str_filename):
        """Read from .cat, merge duplicates (quanta considered unique)"""
        
        with open(str_filename, 'r') as f:
            obj_parser = EgyConverter(self.__bol_respect_parity)
            
            for str_state in f:
                str_q = obj_parser.quanta(str_state)
                
                obj_line = __dict_upper_to_line[str_q]
                obj_parser.update_line(obj_line.state_upper, str_state)
                obj_parser.update_line(obj_line.state_lower, str_state)
                 
    
    def write_cat(self, str_filename):
        """docstring"""
        
        with open(str_filename, 'w') as f:
            lst_lines = self.__dict_upper_to_line.values()
            lst_lines.sort(key=lambda x: x.flt_freq)
            
            obj_writer = CatConverter(self.__bol_respect_parity)
            for obj_line in lst_lines:
                f.write(obj_writer.render_line(obj_line))
                
                
    
