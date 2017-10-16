# python 2.7
#
# Version 1
#

from collections import defaultdict

MINUS = '-'

class 

class State:
    """Additional object of a quantum state"""
    
    def __init__(self):
            self.valid = False

            # support of blends
            self.lst_blends = []

            # energy
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
            
            # quanta and energy
            self.str_ql_l  = ""
            self.str_ql_u  = ""
            self.flt_E_low = None
            self.int_g_up  = 0
            
            # support of blends
            self.lst_blends = []
            
            # Frequency of the line (usually in MHz)
            self.flt_freq      = None           
            self.flt_freq_err  = None

            # base10 log of the integrated intensity at 300 K (in nm2MHz)
            self.flt_log_I        = 0  
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
        
        return self.str_ql_u.split(',')[int_idx]
    
    def qn_lower(self, int_idx):
        """get lower quantum number l[int_idx] as str"""
        
        return self.str_ql_l.split(',')[int_idx]
                        
                        
class CatConverter:
    """Manages entries of .cat files"""
    
    def __init__(self, bol_respect_parity):
        """docstring"""
        
        self.__bol_respect_parity = bol_respect_parity
    
    
    def quanta(self, str_line):
        """get quanta in "x,x;y,y" format"""
        
        return ";".join(self.__read_quanta(str_line))
    
    
    def __replace_cat_quant_digits(self, str_q, bol_reverse):
        """replace a -> -1, A -> 10, etc."""
        
        LST_MAPPING = [ ('a', '-1'), ('b', '-2'), ('c', '-3'), ('d', '-4'), 
                        ('e', '-5'), ('P', '25'), ('f', '-6'), ('g', '-7'),
                        ('h', '-8'), ('i', '-9'), ('j', '-10'), ('k', '-11'),
                        ('l', '-12'), ('m', '-13'), ('n', '-14'), ('o', '-15'),
                        ('p', '-16'), ('A', '10'), ('B', '11'), ('C', '12'), 
                        ('D', '13'), ('E', '14'), ('F', '15'), ('G', '16'), 
                        ('H', '17'), ('I', '18'), ('J', '19'), ('K', '20'), 
                        ('L', '21'), ('M', '22'), ('N', '23'), ('O', '24') ]      
        
        if not bol_reverse:
            dict_map = dict([(x,y) for (x,y) in LST_MAPPING]):
            
            str_s = str_q[0:1]
            if(str_s in dict_map):
                str_q = str_q.replace(str_s, dict_map[str_s])
        else:
            dict_map = dict([(y,x) for (x,y) in LST_MAPPING]):
            
            if len(str_q) >= 3:
            str_s = str_q[0:2]
            if(str_s in dict_map):
                str_q = str_q.replace(str_s, dict_map[str_s])               
        
        return str_q
    
    
    def __read_quanta(self, str_l):
        """convert quanta from .cat to "x,x" format
           returns tuple(str_upper, str_lower) 
           disrespects parity, if needed"""
        
        str_lq   = str_line[55:79]
        str_lq_l = ""
        str_lq_u = ""
        
        INT_C = 6
        INT_S = 2
        for i in range(0, INT_C):
            
            str_q_u = str_lq[i*INT_S : (i+1)*INT_S]
            str_q_l = str_lq[(i+INT_C)*INT_S: (i+INT_C+1)*INT_S]
            
            if str_q_u != "  " and str_q_l != "  ":
                str_q_u   = self.__replace_cat_quant_digits(str_q_u, False)
                str_q_l   = self.__replace_cat_quant_digits(str_q_l, False)
                
                str_lq_l += str_q_l
                str_lq_u += str_q_u
                
                if(i < INT_C - 1):
                    str_lq_l += ","
                    str_lq_u += ","
                    
        return (str_lq_u, str_lq_l)
    
    
    def __write_quanta(self, tup_q)
        """convert quanta from ("x,x","y,y") to .cat str"""

        INT_C = 6
        str_lq = []    
        str_lq_u, str_lq_l = tup_q
        
        for str_q in str_lq_u.split(","):
            str_q   = self.__replace_cat_quant_digits(str_q, True)
            str_lq += str_q   
        for i in range(len(str_lq_u), INT_C):
            str_lq += "  "
        
        for str_q in str_lq_l.split(","):
            str_q   = self.__replace_cat_quant_digits(str_q, True)
            str_lq += str_q   
        for i in range(len(str_lq_l), INT_C):
            str_lq += "  "
        
        return str_lq
    
    
    def update_line(self, str_line, obj_line):
        """str to Line object"""
        
        try:
            bol_success = True
            
            obj_line.flt_freq     = float(str_line[0:13])           
            obj_line.flt_freq_err = float(str_line[13:21])

            obj_line.flt_log_I       = float(str_line[21:29]) 
            obj_line.flt_deg_freedom = int(str_line[29:31])
            
            if not obj_line.state_lower.flt_E:
                obj_line.state_lower.flt_E = float(str_line[31:41])       
                
            obj_line.state_upper.int_g = int(str_line[41:44])
            
            if not obj_line.str_cat_tag:
                obj_line.str_cat_tag       = str_line[44:55]
                obj_line.bol_lab = (MINUS in obj_line.str_tag_cat)
            
            if( not obj_line.state_lower.str_quanta 
             or not obj_line.state_lower.str_quanta ):
                str_lq_u, str_lq_l = self.__read_quanta(str_line)
                obj_line.state_lower.str_quanta = str_lq_l
                obj_line.state_upper.str_quanta = str_lq_u
            
        except:
            bol_success = False
            
        finally:
            return bol_success
        
        
    def render_line(self, obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_quanta = self.__write_quanta((obj_line.state_upper.str_quanta,
                                          obj_line.state_lower.str_quanta))
        
        str_out += "%13.4f%8.4f"% (obj_line.flt_freq, obj_line.freqErr)
        str_out += "%8.4f%2d"   % (obj_line.flt_log_I, obj_line.int_deg_freedom)
        str_out += "%10.4f%3d"  % (obj_line.state_lower.flt_E, obj_line.int_g)
        str_out += "%s%s "      % (obj_line.str_cat_tag, str_quanta)
               
        return str_out



class EgyConverter:
    """Manages entries of .egy files"""
    
    def __init__(self, bol_respect_parity):
        """docstring"""
        
        self.__bol_respect_parity = bol_respect_parity
    
    
    def quanta(self, str_line):
        """get the unque quanta of transition in std format"""
        
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



class CatalogEntry:
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
                
                
    
