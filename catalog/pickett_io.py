# python 2.7
#
# classes:   State, Line, CatConverter, EgyConverter
# functions: load_cat, save_cat, load_egy, save_egy


class Mapper(object):
    """Dictionary forth and reverse transform"""
    
    def __init__(self, a2b):
        if(isinstance(a2b, dict)):
            self.a2b = a2b
            self.b2a = dict( (v,k) for k, v in dict_a2b.items() )
        elif(isinstance(a2b, list):
            self.a2b = dict([(x,y) for (x,y) in a2b]
            self.b2a = dict([(y,x) for (x,y) in a2b])



class State(object):
    """Structure of a quantum state"""
    
    def __init__(self):
            object.__init__(self)
            self.valid = False
            
            # energy
            self.E       = None       
            self.E_err   = None
            self.g       = None
            
            # additional .egy file information
            self.str_H_iblk  = None
            self.str_H_indx  = None
            self.str_pmix    = None
            
            # quantum numbers
            self.quanta      = {}
            self.int_fmt     = None
    
    def has_quanta(self, quanta_subset):
        """Checks if state has these quanta as a subset"""
        
        return all(x in self.quanta.items()
                   for x in quanta_subset.items())
                   


class Line(object):
    """A spectroscopic line entry object"""
    
    def __init__(self):
        self.valid = False
        
        # states
        self.state_upper        = State()
        self.state_lower        = State()
                               
        # Frequency of the line (usually in MHz)
        self.freq           = None
        self.freq_err       = None

        # base10 log of the integrated intensity at 300 K (in nm2MHz)
        self.log_I          = None  
        self.int_deg_freedom    = None
        
        # additional .cat file information
        self.str_cat_tag        = None
        self.bol_lab            = None
        
        # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
        self.flt_pressure_alpha = None    
        self.flt_pressure_delta = None  
        
        # calculated values
        self.Einstein_A     = None
    
    
    # references to upper state g and lower state E and quanta
    def _get_E(self): 
        return self.state_lower.E
        
    def _set_E(self,x): 
        self.state_lower.E = x
        
    def _get_g(self): 
        return self.state_upper.g
        
    def _set_g(self,x):
        self.state_upper.g = x  
        
    def _get_qu(self): 
        return self.state_upper.quanta
        
    def _set_qu(self,x): 
        self.state_upper.quanta = x
        
    def _get_ql(self): 
        return self.state_lower.quanta
        
    def _set_ql(self,x): 
        self.state_lower.quanta = x
        
    def _get_fmt(self): 
        return self.state_upper.int_fmt
        
    def _set_fmt(self,x): 
        self.state_upper.int_fmt = x
        self.state_lower.int_fmt = x
    
    E = property(_get_E, _set_E)
    g = property(_get_g, _set_g)  
    q_upper = property(_get_qu, _set_qu)
    q_lower = property(_get_ql, _set_ql)
    int_fmt = property(_get_fmt, _set_fmt)



class PickettConverter:

    @staticmethod
    def _quanta_headers(int_fmt):
        """returns list of quantum number names for a Pickett code"""
        
        int_c = int_fmt  % 10
        int_Q = int_fmt // 100
        
        DICT_MAPPING = {2:  ['N', 'K', 'J', 'F1', 'F2', 'F'],
                        13: ['N', 'K', 'v', 'J', 'F1', 'F']
                       }
                       
        return DICT_MAPPING[int_Q][0:int_c]



class CatConverter(PickettConverter):
    """Manages entries of .cat files"""
    
    @staticmethod
    def __replace_quant_digits(str_q, bol_reverse):
        """replace a -> -1, A -> 10, etc."""
        
        mapper=Mapper([ ('a', '-1'), ('b', '-2'), ('c', '-3'), ('d', '-4'), 
                        ('e', '-5'), ('P', '25'), ('f', '-6'), ('g', '-7'),
                        ('h', '-8'), ('i', '-9'), ('j', '-10'), ('k', '-11'),
                        ('l', '-12'), ('m', '-13'), ('n', '-14'), ('o', '-15'),
                        ('p', '-16'), ('A', '10'), ('B', '11'), ('C', '12'), 
                        ('D', '13'), ('E', '14'), ('F', '15'), ('G', '16'), 
                        ('H', '17'), ('I', '18'), ('J', '19'), ('K', '20'), 
                        ('L', '21'), ('M', '22'), ('N', '23'), ('O', '24') ])      
        
        if not bol_reverse:
            str_s = str_q[0:1]
            if str_s in mapper.a2b:
                str_q = str_q.replace(str_s, mapper.a2b[str_s])
        else:
            if len(str_q) >= 3:
                str_s = str_q[0:2]
                if(str_s in mapper.b2a):
                    str_q = str_q.replace(str_s, mapper.b2a[str_s])               
        
        return str_q
    
    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .cat to dict 
           returns (dict_upper, dict_lower) 
        """
        dict_ql = {}
        dict_qu = {}
        
        INT_C = 6
        for i in range(0, INT_C):
            
            str_qu = str_quanta[i*2 : (i+1)*2]
            str_ql = str_quanta[(i+INT_C)*2: (i+INT_C+1)*2]
            
            if str_qu != "  " and str_ql != "  ":
                str_qu = CatConverter.__replace_quant_digits(str_qu, False)
                str_ql = CatConverter.__replace_quant_digits(str_ql, False)
                
                headers = CatConverter._quanta_headers(int_fmt)
                dict_ql[headers[i]] = int(str_ql)
                dict_qu[headers[i]] = int(str_qu)
            else:
                break
        
        return (dict_qu, dict_ql)
    
    @staticmethod
    def __write_quanta(tup_q, int_fmt):
        """convert quanta from (dict,dict) to .cat str"""

        INT_C = 6
        str_quanta = ""    
        dict_qu, dict_ql = tup_q
        
        headers = EgyConverter._quanta_headers(int_fmt)[0:len(dict_qu)]
        for str_q in ["%2d" % dict_qu[x] for x in headers]:
            str_q = CatConverter.__replace_quant_digits(str_q, True)
            str_quanta += str_q   
        for i in range(len(dict_qu), INT_C):
            str_quanta += "  "
        
        headers = EgyConverter._quanta_headers(int_fmt)[0:len(dict_ql)]
        for str_q in ["%2d" % dict_ql[x] for x in headers]:
            str_q = CatConverter.__replace_quant_digits(str_q, True)
            str_quanta += str_q   
        for i in range(len(dict_ql), INT_C):
            str_quanta += "  "
        
        return str_quanta
    
    @staticmethod
    def str2line(str_line):
        """str to Line object"""
        
        obj_line = Line()
        try:
            obj_line.valid = True
            
            obj_line.freq     = float(str_line[0:13])           
            obj_line.freq_err = float(str_line[13:21])
            
            obj_line.log_I       = float(str_line[21:29]) 
            obj_line.int_deg_freedom = int(str_line[29:31])
            
            obj_line.E = float(str_line[31:41])           
            obj_line.g = int(str_line[41:44])
            
            obj_line.str_cat_tag       = str_line[44:51]
            obj_line.bol_lab = ('-' in obj_line.str_cat_tag)
            
            str_lq  = str_line[55:79]
            int_fmt = int(str_line[51:55])
            dict_qu, dict_ql = CatConverter.__read_quanta(str_lq, int_fmt)
            
            obj_line.q_upper = dict_qu
            obj_line.q_lower = dict_ql
            obj_line.int_fmt = int_fmt
            
        except Exception as e:
            obj_line.valid = False
            print(e)
            
        finally:
            return obj_line
        
    @staticmethod    
    def line2str(obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_quanta = CatConverter.__write_quanta((obj_line.q_upper,
                                                  obj_line.q_lower),
                                                  obj_line.int_fmt)
        
        str_out += "%13.4f%8.4f"% (obj_line.freq, obj_line.freq_err)
        str_out += "%8.4f%2d"   % (obj_line.log_I, obj_line.int_deg_freedom)
        str_out += "%10.4f%3d"  % (obj_line.E, obj_line.g)
        str_out += "%s%4d%s "      % (obj_line.str_cat_tag, obj_line.int_fmt, str_quanta)
               
        return str_out



class EgyConverter(PickettConverter):
    """Manages entries of .egy files."""
    
    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .egy to dict 
        """
        dict_q = {}
        
        headers = EgyConverter._quanta_headers(int_fmt)
        INT_C = min(int_fmt % 10, len(str_quanta) // 3)
        for i in range(0, INT_C):
            str_q = str_quanta[i*3 : (i+1)*3]
            dict_q[headers[i]] = int(str_q)
        
        return dict_q
    
    @staticmethod
    def __write_quanta(dict_q, int_fmt):
        """convert quanta from dict to .egy str"""

        str_quanta = ""    
        
        headers = EgyConverter._quanta_headers(int_fmt)[0:len(dict_q)]
        for str_q in ["%3d" % dict_q[x] for x in headers]:
            str_quanta += str_q   
        
        return str_quanta
    
    @staticmethod
    def str2state(str_state, int_fmt):
        """str to State object (needs Pickett quanta format code)"""
        
        obj_state = State()
        try:
            obj_state.valid = True
            
            obj_state.str_H_iblk = (str_state[0:6])
            obj_state.str_H_indx = (str_state[6:11])
            
            obj_state.E      = float(str_state[11:29])       
            obj_state.E_err  = float(str_state[29:47])
            
            obj_state.str_pmix   = (str_state[47:58])
            
            obj_state.quanta=EgyConverter.__read_quanta(str_state[64:], int_fmt)
            obj_state.g      = int(str_state[58:63])
        except Exception as e:
            obj_state.valid = False
            print(e)
        finally:
            return obj_state
        
    @staticmethod    
    def state2str(obj_state, int_fmt):
        """Line object to str (needs Pickett quanta format code)"""
        
        str_out = ""
        
        str_out += "%s%s"         % (obj_state.str_H_iblk, obj_state.str_H_indx)
        str_out += "%18.6f%18.6f" % (obj_state.E, obj_state.E_err)
        str_out += "%s%5d:"       % (obj_state.str_pmix, obj_state.g)
        str_out += EgyConverter.__write_quanta(obj_state.quanta, int_fmt) 
        
        return str_out



def load_cat(str_filename):
    """Read from .cat"""
    
    lst_lines  = []
    with open(str_filename, 'r') as f:
        for str_line in f:
            obj = CatConverter.str2line(str_line)
            lst_lines.append(obj)
        
    return lst_lines


def get_quantum_fmt(str_filename):
    """Get the FMT from .cat file"""
    
    int_quanta_fmt = None
    with open(str_filename, 'r') as f:
        str_line = f.readline()
        obj_line = CatConverter.str2line(str_line)
        int_quanta_fmt = obj_line.int_fmt
    
    return int_quanta_fmt
    

def load_egy(str_filename, int_quanta_fmt):
    """Read from .egy"""
    
    lst_states  = []
    with open(str_filename, 'r') as f:
        for str_state in f:
            obj = EgyConverter.str2state(str_state, int_quanta_fmt)
            lst_states.append(obj)
    
    return lst_states


def save_cat(str_filename, lst_lines):
    """docstring"""
    
    with open(str_filename, 'w') as f:
        for obj_line in lst_lines:
            textline = CatConverter.line2str(obj_line)
            f.write(textline+"\n")


def save_egy(str_filename, lst_states, int_quanta_fmt):
    """docstring"""
    
    with open(str_filename, 'w') as f:
        for obj_state in lst_states:
            textline = EgyConverter.state2str(obj_state, int_quanta_fmt)
            f.write(textline+"\n")


