# python 2.7
#
# classes: State, Line
#

class State:
    """Structure of a quantum state"""
    
    def __init__(self):
            self.valid = False
            
            # energy
            self.flt_E       = None       
            self.flt_E_err   = None
            self.int_g       = None
            
            # additional .egy file information
            self.str_H_iblk  = None
            self.str_H_indx  = None
            self.str_pmix    = None
            
            # quantum numbers
            self.dict_quanta = {}
            self.int_fmt     = None
    
    def has_quanta(self, dict_quanta_subset):
        """Checks if state has these quanta as a subset"""
        
        return all(x in self.dict_quanta.items()
                   for x in dict_quanta_subset.items())


class Line:
    """A spectroscopic line entry object"""
    
    def __init__(self):
            self.valid = False
            
            # states
            self.state_upper        = State()
            self.state_lower        = State()
            
            # Frequency of the line (usually in MHz)
            self.flt_freq           = None
            self.flt_freq_err       = None

            # base10 log of the integrated intensity at 300 K (in nm2MHz)
            self.flt_log_I          = None  
            self.int_deg_freedom    = None
            
            # additional .cat file information
            self.str_cat_tag        = None
            self.bol_lab            = None
            
            # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
            self.flt_pressure_alpha = None    
            self.flt_pressure_delta = None  
            
            # calculated values
            self.flt_Einstein_A     = None

