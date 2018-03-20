# python 2,3
#

import copy
from bidict import bidict
from werkzeug.datastructures import MultiDict

class State(object):
    """Structure of a quantum state"""
    
    def __init__(self):
            object.__init__(self)
         
            # energy
            self.E       = None       
            self.E_err   = None
            self.g       = None
            
            # additional .egy file information
            self.str_H_iblk  = None
            self.str_H_indx  = None
            self.str_pmix    = None
            
            # quantum numbers
            self._quanta   = frozenset()
            self.int_fmt   = None
    
    def copy(self):
        return copy.deepcopy(self)
    
    def qid(self):
        """docstring"""
        
        return (self._quanta)
    
    
    def has_quanta(self, quanta_subset):
        """Checks if state has these quanta as a subset"""
        
        return all(x in self.q.items()
                   for x in quanta_subset.items())
                   
    def _get_q(self): 
        return dict(self._quanta)
        
    def _set_q(self,dict_x): 
        self._quanta = frozenset(dict_x.items())
        
    q = property(_get_q, _set_q) 
        
        

class Line(object):
    """A spectroscopic line entry object"""
    
    def __init__(self):
    
        # states
        self.state_upper        = State()
        self.state_lower        = State()
                               
        # Frequency of the line (usually in MHz)
        self.freq            = None
        self.freq_err        = None

        # base10 log of the integrated intensity at 300 K (in nm2MHz)
        self.log_I           = None  
        self.int_deg_freedom = None
        
        # additional information
        self.int_cat_tag     = None
        self.str_lin_text    = None
        
        # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
        self.flt_pressure_alpha = None    
        self.flt_pressure_delta = None  
        
        # calculated values
        self.Einstein_A = None
    
    def copy(self):
        return copy.deepcopy(self)
    
    def qid(self):
        """docstring"""
        
        return ((self.state_upper._quanta, self.state_lower._quanta))

    
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
        return self.state_upper.q
        
    def _set_qu(self,x): 
        self.state_upper.q = x
        
    def _get_ql(self): 
        return self.state_lower.q
        
    def _set_ql(self,x): 
        self.state_lower.q = x
        
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


def qid(q1, q2=None):
    """stand-alone function to create haschable quantum IDs
       used for dictionary lookup. q1, q2 are DICTS like also in other methods
    """
    
    if q2 is None:
        return frozenset(q1.items())
    else:
        return (frozenset(q1.items()), frozenset(q2.items()))


def quanta_headers(int_fmt):
    """returns list of quantum number names for a Pickett code"""
    
    int_c = int_fmt  % 10
    int_Q = int_fmt // 100
    
    DICT_MAPPING = {2:  ['N', 'K', 'J', 'F1', 'F2', 'F'],
                    13: ['N', 'K', 'v', 'J', 'F1', 'F']
                   }
                   
    return DICT_MAPPING[int_Q][0:int_c]


class CatConverter:
    """Manages entries of .cat files"""
    
    mapper=bidict([ ('a', '-1'), ('b', '-2'), ('c', '-3'), ('d', '-4'), 
                ('e', '-5'), ('P', '25'), ('f', '-6'), ('g', '-7'),
                ('h', '-8'), ('i', '-9'), ('j', '-10'), ('k', '-11'),
                ('l', '-12'), ('m', '-13'), ('n', '-14'), ('o', '-15'),
                ('p', '-16'), ('A', '10'), ('B', '11'), ('C', '12'), 
                ('D', '13'), ('E', '14'), ('F', '15'), ('G', '16'), 
                ('H', '17'), ('I', '18'), ('J', '19'), ('K', '20'), 
                ('L', '21'), ('M', '22'), ('N', '23'), ('O', '24') ]) 
    
    @staticmethod
    def __decode_quant(str_q):
        """replace a -> -1, A -> 10, etc."""
        
        str_s = str_q[0:1]
        if str_s in CatConverter.mapper:
            str_q = str_q.replace(str_s, CatConverter.mapper[str_s])
        
        return str_q
    
    
    @staticmethod
    def __encode_quant(str_q):
        """replace -1 -> a, 10 -> A, etc."""
        
        if len(str_q) >= 3:
            str_s = str_q[0:2]
            if(str_s in CatConverter.mapper.inv):
                str_q = str_q.replace(str_s, CatConverter.mapper.inv[str_s])               
        
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
                str_qu = CatConverter.__decode_quant(str_qu)
                str_ql = CatConverter.__decode_quant(str_ql)
                
                headers = quanta_headers(int_fmt)
                dict_ql[headers[i]] = int(str_ql)
                dict_qu[headers[i]] = int(str_qu)
            else:
                break
        
        return (dict_qu, dict_ql)
    
    @staticmethod
    def __write_quanta(dict_qu, dict_ql, int_fmt):
        """convert quanta from (dict,dict) to .cat str"""

        INT_C = 6
        str_quanta = ""    
        
        headers = quanta_headers(int_fmt)[0:len(dict_qu)]
        for str_q in ["%2d" % dict_qu[x] for x in headers]:
            str_q = CatConverter.__encode_quant(str_q)
            str_quanta += str_q   
        for i in range(len(headers), INT_C):
            str_quanta += "  "
        
        headers = quanta_headers(int_fmt)[0:len(dict_ql)]
        for str_q in ["%2d" % dict_ql[x] for x in headers]:
            str_q = CatConverter.__encode_quant(str_q)
            str_quanta += str_q   
        for i in range(len(headers), INT_C):
            str_quanta += "  "
        
        return str_quanta
    
    @staticmethod
    def str2line(str_line):
        """str to Line object"""
        
        obj_line = Line()
        
        obj_line.freq     = float(str_line[0:13])           
        obj_line.freq_err = float(str_line[13:21])
        
        obj_line.log_I       = float(str_line[21:29]) 
        obj_line.int_deg_freedom = int(str_line[29:31])
        
        obj_line.E = float(str_line[31:41])           
        obj_line.g = int(str_line[41:44])
        
        obj_line.int_cat_tag  = int(str_line[44:51])
        
        str_q  = str_line[55:79]
        int_fmt = int(str_line[51:55])
        dict_qu, dict_ql = CatConverter.__read_quanta(str_q, int_fmt)
        
        obj_line.q_upper = dict_qu
        obj_line.q_lower = dict_ql
        obj_line.int_fmt = int_fmt
            
        return obj_line
        
    @staticmethod    
    def line2str(obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_quanta = CatConverter.__write_quanta(obj_line.q_upper,
                                                  obj_line.q_lower,
                                                  obj_line.int_fmt)
        
        str_out += "%13.4f%8.4f"% (obj_line.freq, obj_line.freq_err)
        str_out += "%8.4f%2d"   % (obj_line.log_I, obj_line.int_deg_freedom)
        str_out += "%10.4f%3d"  % (obj_line.E, obj_line.g)
        str_out += "%7d"        % (obj_line.int_cat_tag)
        str_out += "%4d%s "     % (obj_line.int_fmt, str_quanta)
               
        return str_out



class EgyConverter:
    """Manages entries of .egy files."""
    
    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .egy to dict 
        """
        dict_q = {}
        
        headers = quanta_headers(int_fmt)
        INT_C = min(int_fmt % 10, len(str_quanta) // 3)
        for i in range(0, INT_C):
            str_q = str_quanta[i*3 : (i+1)*3]
            dict_q[headers[i]] = int(str_q)
        
        return dict_q
    
    @staticmethod
    def __write_quanta(dict_q, int_fmt):
        """convert quanta from dict to .egy str"""

        str_quanta = ""    
        
        headers = quanta_headers(int_fmt)[0:len(dict_q)]
        for str_q in ["%3d" % dict_q[x] for x in headers]:
            str_quanta += str_q   
        
        return str_quanta
    
    @staticmethod
    def str2state(str_state, int_fmt):
        """str to State object (needs Pickett quanta format code)"""
        
        obj_state = State()
            
        obj_state.str_H_iblk = (str_state[0:6])
        obj_state.str_H_indx = (str_state[6:11])
        
        obj_state.E      = float(str_state[11:29])       
        obj_state.E_err  = float(str_state[29:47])
        
        obj_state.str_pmix   = (str_state[47:58])
        
        obj_state.int_fmt = int_fmt
        obj_state.q = EgyConverter.__read_quanta(str_state[64:], int_fmt)
        obj_state.g = int(str_state[58:63])
        
        return obj_state
        
    @staticmethod    
    def state2str(obj_state):
        """Line object to str (needs Pickett quanta format code)"""
        
        str_out = ""
        
        str_out += "%s%s"         % (obj_state.str_H_iblk, obj_state.str_H_indx)
        str_out += "%18.6f%18.6f" % (obj_state.E, obj_state.E_err)
        str_out += "%s%5d:"       % (obj_state.str_pmix, obj_state.g)
        str_out += EgyConverter.__write_quanta(obj_state.q, obj_state.int_fmt) 
        
        return str_out



class LinConverter:
    """Manages entries of .lin files"""
    
    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .cat to dict 
           returns (dict_upper, dict_lower) 
        """
        dict_ql = {}
        dict_qu = {}
        
        INT_C = int_fmt % 10
        for i in range(0, INT_C):
            
            str_qu = str_quanta[i*3 : (i+1)*3]
            str_ql = str_quanta[(i+INT_C)*3: (i+INT_C+1)*3]
            
            headers = quanta_headers(int_fmt)
            dict_ql[headers[i]] = int(str_ql)
            dict_qu[headers[i]] = int(str_qu)
        
        return (dict_qu, dict_ql)
    
    @staticmethod
    def __write_quanta(dict_qu, dict_ql, int_fmt):
        """convert quanta from (dict,dict) to .cat str"""
        
        INT_C_MAX  = 6
        INT_C      = int_fmt % 10
        str_quanta = ""   
        
        headers = quanta_headers(int_fmt)[0:len(dict_qu)]
        for str_q in ["%3d" % dict_qu[x] for x in headers]:
            str_quanta += str_q   
        for i in range(len(headers), INT_C):
            str_quanta += "   "
        
        headers = quanta_headers(int_fmt)[0:len(dict_ql)]
        for str_q in ["%3d" % dict_ql[x] for x in headers]:
            str_quanta += str_q   
        for i in range(len(headers), INT_C):
            str_quanta += "   "
        
        for i in range(2*INT_C, 2*INT_C_MAX):
            str_quanta += "   "
        
        return str_quanta
    
    @staticmethod
    def str2line(str_line, int_fmt):
        """str to Line object"""
        
        obj_line = Line()
        obj_line.freq     = float(str_line[36:51])           
        obj_line.freq_err = float(str_line[51:60])
        
        obj_line.str_lin_text = str_line[60:-1]
        
        str_q  = str_line[0:36]
        dict_qu, dict_ql = LinConverter.__read_quanta(str_q, int_fmt)
        
        obj_line.int_fmt = int_fmt
        obj_line.q_upper = dict_qu
        obj_line.q_lower = dict_ql
            
        return obj_line
        
    @staticmethod    
    def line2str(obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_quanta = LinConverter.__write_quanta(obj_line.q_upper,
                                                 obj_line.q_lower,
                                                 obj_line.int_fmt)

        str_out += "%s"    % (str_quanta)
        str_out += "%15.4f"% (obj_line.freq)
        str_out +=("%10.3f"% (obj_line.freq_err)).replace('0.', '.')
        str_out += "%s"    % (obj_line.str_lin_text)
              
        return str_out



def get_quantum_fmt(str_filename):
    """Get the FMT from .cat file"""
    
    int_quanta_fmt = None
    with open(str_filename, 'r') as f:
        str_line = f.readline()
        obj_line = CatConverter.str2line(str_line)
        int_quanta_fmt = obj_line.int_fmt
    
    return int_quanta_fmt


def load_cat(str_filename):
    """Read from .cat"""
    
    lst_lines  = []
    with open(str_filename, 'r') as f:
        for str_line in f:
            obj = CatConverter.str2line(str_line)
            lst_lines.append(obj)
        
    return lst_lines


def save_cat(str_filename, lst_lines):
    """docstring"""
    
    with open(str_filename, 'w') as f:
        for obj_line in lst_lines:
            textline = CatConverter.line2str(obj_line)
            f.write(textline+"\n")


def load_lin(str_filename, int_quanta_fmt):
    """Read from .cat"""
    
    lst_lines  = []
    with open(str_filename, 'r') as f:
        for i, str_line in enumerate(f):
            try:
                obj = LinConverter.str2line(str_line, int_quanta_fmt)
                lst_lines.append(obj)
            except(ValueError):
                print ('Warning: skipping bad line %i' % (i+1)) 
        
    return lst_lines


def save_lin(str_filename, lst_lines):
    """docstring"""
    
    with open(str_filename, 'w') as f:
        for obj_line in lst_lines:
            textline = LinConverter.line2str(obj_line)
            f.write(textline+"\n")


def load_egy(str_filename, int_quanta_fmt):
    """Read from .egy"""
    
    lst_states  = []
    with open(str_filename, 'r') as f:
        for str_state in f:
            obj = EgyConverter.str2state(str_state, int_quanta_fmt)
            lst_states.append(obj)
    
    return lst_states
    

def save_egy(str_filename, lst_states):
    """docstring"""
    
    with open(str_filename, 'w') as f:
        for obj_state in lst_states:
            textline = EgyConverter.state2str(obj_state)
            f.write(textline+"\n")


class Formatter:
    """formatting methods on transitions and states"""
    
    def __init__(self, corrector = None):
        self.__model = corrector
    
    def custom_quanta_transform(self, entries, func_transform):
        """docstring"""

        for entry in entries:
            if hasattr(entry, "q"):
                entry.q = func_transform(entry.q)
                
            elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
                entry.q_upper = func_transform(entry.q_upper)
                entry.q_lower = func_transform(entry.q_lower)
    
    
    def correct(self, entries, file_format):
        """Corrects wrong splits or blends
           Works only if 'corrector' is not None and implements:
            find_mergable_with_state(states, state)
            find_mergable_with_line(lines, line)
            merge_lines(blends)
            merge_states(blends)
            split_line(lines, line, flag_require_all_spilts) 
            split_state(states, state)
        """        
        
        # make O(1) lookup dict 
        dict_entries = self.__build_dict(entries)
        
        # merge blends (assumption: entries partitioned into mergable classes)
        result  = []
        ignore  = set()
        for cur in entries:
            
            if cur.qid() in ignore:
                continue
            
            blends = self.__find_mergable(dict_entries, cur, file_format)
            
            if(len(blends) > 1):
                result.append(self.__merge(blends, file_format))
                ignore.update([x.qid() for x in blends])
            else:
                result.append(cur)
                ignore.add(cur.qid())
                
        # make splits        
        result2  = []
        for cur in result:
            
            splits = self.__split(dict_entries, cur, file_format)
        
            result2.extend(splits)
            
            dict_entries.update(self.__build_dict(splits))
        
        return result2
    
    
    def make_mrg(self, cat_lst, lin_lst, egy_lst = []):
        """look for cat entries in lin and merge the two files into mrg"""
        
        result = []
        
        lin_dict = self.__build_dict(lin_lst)
        
        for entry_cat in cat_lst:
            entry_mrg = entry_cat.copy()
            
            if entry_mrg.qid() in lin_dict:
                entry_lin = lin_dict[entry_mrg.qid()]
                
                entry_mrg.freq = entry_lin.freq
                entry_mrg.freq_err = entry_lin.freq_err
                entry_mrg.int_cat_tag = -abs(entry_mrg.int_cat_tag)
                
            result.append(entry_mrg)
        
        return result
    
    
    def __find_mergable(self, dict_entries, cur, file_format):
        
        if 'cat' in file_format or 'lin' in file_format:
            return self.__model.find_mergable_with_line(dict_entries, cur)
        elif 'egy' in file_format:
            return self.__model.find_mergable_with_state(dict_entries, cur)
        else:
            raise Exception('File format unknown') 
    
    
    def __merge(self, blends, file_format):
        
        if 'cat' in file_format or 'lin' in file_format:
            return self.__model.merge_lines(blends)
        elif 'egy' in file_format:
            return self.__model.merge_states(blends)
        else:
            raise Exception('File format unknown') 
    

    def __split(self, dict_entries, cur, file_format):
        
        if 'cat' in file_format:
            return self.__model.split_line(dict_entries, cur, flag_require_all_spilts=True)
        elif 'lin' in file_format:
            return self.__model.split_line(dict_entries, cur, flag_require_all_spilts=False)
        elif 'egy' in file_format:
            return self.__model.split_state(dict_entries, cur)
        else:
            raise Exception('File format unknown') 
        
    
    def __build_dict(self, entries):
        """docstring"""
        
        result = MultiDict()
        for e in entries:
            result.add(e.qid(), e)
            
        return result
    
        
        
