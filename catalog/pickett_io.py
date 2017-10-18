# python 2.7
#
# classes: CatConverter, EgyConverter
#

def __quanta_headers(int_fmt):
    """returns list of quantum number names for a Pickett code"""
    
    int_c = int_fmt  % 10
    int_Q = int_fmt // 100
    
    DICT_MAPPING = {2:  ['N', 'K', 'J', 'F1', 'F2', 'F']
                    13: ['N', 'K', 'v', 'J', 'F1', 'F']
                   }
                   
    return DICT_MAPPING[int_Q][0:int_c]


class CatConverter:
    """Manages entries of .cat files"""
    
    def __init__(self):
        """docstring"""
        pass
    
    def __replace_quant_digits(self, str_q, bol_reverse):
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
    
    
    def __read_quanta(self, str_quanta, int_fmt):
        """convert quanta from .cat to dict 
           returns (dict_upper, dict_lower) 
        """
        dict_ql = {}
        dict_qu = {}
        
        INT_C = 6
        for i in range(0, INT_C):
            
            str_qu = str_quanta[i*2 : (i+1)*2]
            str_ql = str_quanta[(i+INT_C)*2: (i+INT_C+1)*2]
            
            if str_q_u != "  " and str_q_l != "  ":
                str_qu = self.__replace_quant_digits(str_qu, False)
                str_ql = self.__replace_quant_digits(str_ql, False)
                
                dict_ql[__quanta_headers(int_fmt)[i]] = int(str_ql)
                dict_qu[__quanta_headers(int_fmt)[i]] = int(str_qu)
            else:
                break
        
        return (dict_qu, dict_ql)
    
    
    def __write_quanta(self, tup_q, int_fmt)
        """convert quanta from (dict,dict) to .cat str"""

        INT_C = 6
        str_quanta = ""    
        dict_qu, dict_ql = tup_q
        
        for str_q in ["%2d" % dict_qu[x] for x in __quanta_headers(int_fmt)]:
            str_q = self.__replace_quant_digits(str_q, True)
            str_quanta += str_q   
        for i in range(len(dict_qu), INT_C):
            str_quanta += "  "
        
        for str_q in ["%2d" % dict_ql[x] for x in __quanta_headers(int_fmt)]:
            str_q = self.__replace_quant_digits(str_q, True)
            str_quanta += str_q   
        for i in range(len(dict_ql), INT_C):
            str_quanta += "  "
        
        return str_quanta
    
    
    def str2line(self, str_line):
        """str to Line object"""
        
        obj_line = Line()
        try:
            obj_line.valid = True
            
            obj_line.flt_freq     = float(str_line[0:13])           
            obj_line.flt_freq_err = float(str_line[13:21])

            obj_line.flt_log_I       = float(str_line[21:29]) 
            obj_line.flt_deg_freedom = int(str_line[29:31])
            
            obj_line.state_lower.flt_E = float(str_line[31:41])       
            obj_line.state_upper.int_g = int(str_line[41:44])
            
            obj_line.str_cat_tag       = str_line[44:51]
            obj_line.bol_lab = ('-' in obj_line.str_tag_cat)
            
            str_lq  = str_line[55:79]
            int_fmt = int(str_line[51:55])
            dict_qu, dict_ql = self.__read_quanta(str_lq, int_fmt)
            
            obj_line.state_upper.dict_quanta = dict_qu
            obj_line.state_lower.dict_quanta = dict_ql
            obj_line.state_upper.int_fmt = int_fmt
            obj_line.state_lower.int_fmt = int_fmt
            
        except:
            obj_line.valid = False
            
        finally:
            return obj_line
        
        
    def line2str(self, obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_quanta = self.__write_quanta((obj_line.state_upper.dict_quanta,
                                          obj_line.state_lower.dict_quanta),
                                          obj_line.state_upper.int_fmt)
        
        str_out += "%13.4f%8.4f"% (obj_line.flt_freq, obj_line.freqErr)
        str_out += "%8.4f%2d"   % (obj_line.flt_log_I, obj_line.int_deg_freedom)
        str_out += "%10.4f%3d"  % (obj_line.state_lower.flt_E,
                                   obj_line.state_upper.int_g)
        str_out += "%s%s "      % (obj_line.str_cat_tag, str_quanta)
               
        return str_out



class EgyConverter:
    """Manages entries of .egy files.
       EgyConverter.update() must be used after CatConverter.update() 
    """
    
    def __init__(self):
        """docstring"""
        pass
    
    def __read_quanta(self, str_quanta, int_fmt):
        """convert quanta from .egy to dict 
        """
        dict_q = {}
        
        INT_C = int_fmt % 10
        for i in range(0, INT_C):
            str_q = str_quanta[i*3 : (i+1)*3]
            dict_q[__quanta_headers(int_fmt)[i]] = int(str_q)
        
        return dict_q
    
    
    def __write_quanta(self, dict_q, int_fmt)
        """convert quanta from dict to .egy str"""

        str_quanta = ""    
        
        for str_q in ["%3d" % dict_q[x] for x in __quanta_headers(int_fmt)]:
            str_quanta += str_q   
        
        return str_quanta
    
    
    def str2state(self, str_state, int_fmt):
        """str to State object (needs Pickett quanta format code)"""

        obj_state = State()
        try:
            obj_state.valid = True
            
            obj_state.str_H_iblk = (str_state[0:6])
            obj_state.str_H_indx = (str_state[6:11])
            
            obj_state.flt_E      = float(str_state[11:29])       
            obj_state.flt_E_err  = float(str_state[29:47])
            
            obj_state.str_pmix   = (str_state[47:58])
            
            obj_state.dict_quanta= self.__read_quanta(str_line[64:], int_fmt)
            obj_state.int_g      = int(str_state[58:63]
            
        except:
            obj_state.valid = False
            
        finally:
            return obj_state
        
        
    def state2str(self, obj_state, int_fmt):
        """Line object to str (needs Pickett quanta format code)"""
        
        str_out = ""
        
        str_out += "%s%s"         % (obj_state.str_H_iblk, obj_state.str_H_indx)
        str_out += "%18.6f%18.6f" % (obj_state.flt_E, obj_state.flt_E_err)
        str_out += "%s%5d:"       % (obj_state.str_pmix, obj_state.int_g)
        str_out += self.__write_quanta(obj_state.dict_quanta, int_fmt) 
        
        return str_out
