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
                   
    def __eq__(self, other):
        """Equivalence is defined in terms of quanta"""
        
        return self.dic_quanta == other.dict_quanta


class Line:
    """A spectroscopic line entry object"""
    
    def __init__(self):
            self.valid = False
            
            # states
            self.state_upper        = State()
            self.state_lower        = State()
            
            # references to upper state g and lower state E and quanta
            def _get_E(self): 
                return self.state_lower.flt_E
            def _set_E(self): 
                self.state_lower.flt_E = x
            def _get_g(self): 
                return self.state_upper.int_g
            def _set_g(self,x):
                self.state_upper.int_g = x  
            def _get_qu(self): 
                return self.state_upper.dict_quanta
            def _set_qu(self,x): 
                self.state_upper.dict_quanta = x
            def _get_ql(self): 
                return self.state_lower.dict_quanta
            def _set_ql(self,x): 
                self.state_lower.dict_quanta = x
            def _get_fmt(self): 
                return self.state_upper.int_fmt
            def _set_fmt(self,x): 
                self.state_upper.dict_quanta = x
                self.state_lower.dict_quanta = x
            
            self.flt_E = property(_get_E, _set_E)
            self.int_g = property(_get_g, _set_g)  
            self.q_upper = property(_get_qu, _set_qu)
            self.q_lower = property(_get_ql, _set_ql)
            self.int_fmt = property(_get_fmt, _set_fmt)
                                    
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
    
    
    def __eq__(self, other):
        """Equivalence is defined in terms of quanta"""
        
        return self.q_upper == other.q_upper and self.q_lower == other.q_lower