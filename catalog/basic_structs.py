# python 2.7
#
# classes: IQuantaInterpreter, State, Line
#

class IQuantaInterpreter:
    """interface of delegate types to work with quantum numbers"""
    
    def q_eq(self, str_q1, str_q2):
        """Are two sets of quantum numbers equal?"""
        
        raise NotImplementedError
    
    
    def q_in(self, str_q1, str_q2):
        """Is set q1 included in set q2?"""
        raise NotImplementedError
    
    
    def q_blend(self, str_q1, str_q2):
        """Can two quantum objects be blended?"""
        
        raise NotImplementedError


class State:
    """Structure of a quantum state"""
    
    def __init__(self):
            ##self.valid = False
            
            # energy
            self.flt_E       = None       
            self.flt_E_err   = None
            self.int_g       = None
            
            # additional .egy file information
            self.str_H_iblk  = None
            self.str_H_indx  = None
            self.str_pmix    = None
            
            # quantum numbers
            """format is "x,x,x" """
            self.str_quanta  = ""


class Line:
    """A spectroscopic line entry object"""
    
    def __init__(self, obj_quantum_interpreter):
            ##self.valid = False
            
            # states
            self.state_upper        = State(obj_quantum_interpreter)
            self.state_lower        = State(obj_quantum_interpreter)
            
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
     
            
    def qnu(self, int_idx):
        """get upper quantum number u[int_idx] as int"""
        
        return self.state_upper.str_quanta.split(',')[int_idx]
    
    
    def qnl(self, int_idx):
        """get lower quantum number l[int_idx] as int"""
        
        return self.state_lower.str_quanta.split(',')[int_idx]
    
    
    def quanta(self):
        """docstring"""
        
        lst_str_q = [self.state_lower.str_quanta, self.state_upper.str_quanta]
        
        return ";".join(lst_str_q)
    
    
    def set_quanta(self, str_ql):
        """docstring"""
        
        str_lq_l, str_lq_u = str_ql.split(";")
        
        self.state_lower.str_quanta = str_lq_l
        self.state_upper.str_quanta = str_lq_u

