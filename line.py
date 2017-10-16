# python 2.7
#
# Version 1
#

# globals
MINUS = '-'

class State:
    """Additional object of a quantum state"""
    
    def __init__(self):
            self.valid = False

            self.flt_E       = None       
            self.flt_E_err   = None
            self.int_g       = None

            # egy file information
            self.str_hiblk   = None
            self.str_hindx   = None
            self.str_pmix    = None

            # quantum numbers
            self.str_quanta = ""
    

class Line:
    """A line entry object"""
    def __init__(self):
            self.valid = False
            
            # states
            self.state_upper = State()
            self.state_lower = State()
            
            # Frequency of the line (usually in MHz)
            self.flt_freq      = None           
            self.flt_freq_err  = None

            # base10 log of the integrated intensity at 300 K (in nm2MHz)
            self.flt_log_I        = None  
            self.int_deg_freedom  = None
            
            # lower state energy (in cm-1), etc.
            self.flt_Einstein_A = None    
            self.str_cat_tag    = None
            self.bol_lab        = None
            
            # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
            self.flt_pressure_alpha = None    
            self.flt_pressure_delta = None  
     
            
    def qn_upper(self, int_idx):
        """get upper quantum number u[int_idx] as str"""
        
        str_q = self.state_upper.str_quanta

        int_c = len(str_q) / 2
        assert int_idx >= 0 and int_idx < int_c
         
        return str_q[int_idx*2:int_idx*2+2]
    
    
    def qn_lower(self, int_idx):
        """get lower quantum number l[int_idx] as str"""
        
        str_q = self.state_lower.str_quanta

        int_c = len(str_q) / 2
        assert int_idx >= 0 and int_idx < int_c
         
        return str_q[int_idx*2:int_idx*2+2]
                        
                        
class CatConverter:
    """Manages entries of .cat files"""
    
    def quanta_upper(self, str_line):
        """get quanta of transition's upper state"""
        
        return str_line[55:67]


    def quanta_lower(self, str_line):
        """get quanta of transition's lower state"""
        
        return str_line[67:79]
    
    
    def update_line(self, str_line, obj_line):
        """str to Line object"""
        
        try:
            bol_success = True
            
            obj_line.flt_freq     = float(str_line[0:13])           
            obj_line.flt_freq_err = float(str_line[13:21])

            obj_line.flt_log_I       = float(str_line[21:29]) 
            obj_line.flt_deg_freedom = int(str_line[29:31])
            
            obj_line.state_lower.flt_E = float(str_line[31:41])       
            obj_line.state_upper.int_g = int(str_line[41:44])
            obj_line.str_cat_tag       = str_line[44:55]
            
            obj_line.bol_lab = (MINUS in obj_line.str_tag_cat)
            
        except:
            bol_success = False
            
        finally:
            return bol_success
        
        
    def render_line(self, obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_out += "%13.4f%8.4f" % (obj_line.flt_freq, obj_line.freqErr)
        str_out += "%8.4f%2d"    % (obj_line.flt_log_I, obj_line.int_deg_freedom)
        str_out += "%10.4f%3d%s" % (obj_line.state_lower.flt_E, obj_line.int_g, obj_line.str_cat_tag)
        str_out += obj_line.state_upped.str_quanta + obj_line.state_lower.str_quanta + " "
               
        return str_out



class EgyConverter:
    """Manages entries of .egy files"""
    
    def quanta(self, str_line):
        """get the unque quanta of transition"""
        
        return str_line[55:79]
    
    
    def update_state(self, obj_state, str_state):
        """str to Line object (except quanta)"""
        
        try:
            bol_success = True

            obj_state.flt_E     = float(str_state[31:41])       
            obj_state.flt_E_err = float(str_state[41:44])
            
            #FIXME
            
        except:
            bol_success = False
            
        finally:
            return bol_success
        
        
    def render_state(self, obj_state):
        """Line object to str"""
        
        str_out = ""
        #FIXME
        
        str_out += "%13.4f%8.4f" % (obj_line.freq, obj_line.freqErr)
        str_out += "%8.4f%2d"    % (obj_line.logI, obj_line.freedom)
        str_out += "%10.4f%3d%s" % (obj_line.Elow, obj_line.g, obj_line.tag)
        str_out += "".join(obj_line.qUpper) + "".join(obj_line.qLower) + " "
               
        return str_out



class Catalog:
    """docstring"""
    
    def __init__(self):
        """docstring"""
        
        self.__dict_upper_to_line = {}
        self.__dict_lower_to_line = {}
        self.__bol_respect_parity = True
        
        
    def load_cat(self, str_filename):
        """docstring"""
        
        with open(str_filename, 'r') as file:
            obj_parser = CatParser(self.__bol_respect_parity)
            
            for str_line in file:
                str_u = obj_parser.quanta_upper(str_line)
                str_l = obj_parser.quanta_lower(str_line)
                
                obj_line = __dict_upper_to_line.get(str_u, Line())
                obj_parser.update_line(obj_line, str_line)
                
                obj_line = __dict_lower_to_line.get(str_l, Line())
                obj_parser.update_line(obj_line, str_line)

                
    def load_egy(self, str_filename):
        """docstring"""
        
        with open(str_filename, 'r') as file:
            obj_parser = EgyParser()
            
            for str_state in file:
                str_q = obj_parser.quanta(str_state)
                
                obj_line = __dict_upper_to_line.get(str_q, Line())
                obj_parser.update_line(obj_line.state_upper, str_state)
                
                obj_line = __dict_lower_to_line.get(str_q, Line())
                obj_parser.update_line(obj_line.state_lower, str_state)
                 
