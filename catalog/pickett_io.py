# python 2.7
#
# classes: CatConverter, EgyConverter
#

class CatConverter:
    """Manages entries of .cat files"""
    
    def __init__(self, obj_quanta_interpreter):
        """docstring"""
        
        self.__interpeter = obj_quanta_interpreter
    
    
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
    
    
    def update(self, str_line, obj_line):
        """str to Line object"""
        
        try:
            bol_success = True
            
            obj_line.flt_freq     = float(str_line[0:13])           
            obj_line.flt_freq_err = float(str_line[13:21])

            obj_line.flt_log_I       = float(str_line[21:29]) 
            obj_line.flt_deg_freedom = int(str_line[29:31])
            
            if not obj_line.state_lower.flt_E:
                obj_line.state_lower.flt_E = float(str_line[31:41])       
            
            if(obj_line.state_upper.int_g):
                assert obj_line.state_upper.int_g == int(str_line[41:44])
            else:
                obj_line.state_upper.int_g = int(str_line[41:44])
            
            if not obj_line.str_cat_tag:
                obj_line.str_cat_tag       = str_line[44:55]
                obj_line.bol_lab = ('-' in obj_line.str_tag_cat)
            
            str_lq = self.__read_quanta(str_line)
            if( obj_line.quanta() ) 
                assert self.__interpreter.q_in(obj_line.quanta(), str_lq)
            obj_line.set_quanta(str_lq)
            
        except:
            bol_success = False
            
        finally:
            return bol_success
        
        
    def render(self, obj_line):
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
    
    def __init__(self, obj_quanta_interpreter):
        """docstring"""
        
        self.__interpeter = obj_quanta_interpreter
    
    
    def update(self, obj_state, str_state):
        """str to Line object (except quanta)"""
        
        try:
            bol_success = True
            
            obj_state.str_H_iblk = (str_state[0:6])
            obj_state.str_H_indx = (str_state[6:11])
            
            obj_state.flt_E      = float(str_state[11:29])       
            obj_state.flt_E_err  = float(str_state[29:47])
            
            obj_state.str_pmix   = (str_state[47:58])
            
            str_lq_u = self.__read_quanta(str_state)
            if( obj_state.str_quanta ):
                assert self.__interpeter.q_in(obj_state.str_quanta, str_lq)
            obj_state.str_quanta = str_lq
            
            if not obj_state.int_g:
                obj_state.int_g = int(str_state[58:63]
            else:
                assert obj_state.int_g == int(str_state[58:63]                
            
        except:
            bol_success = False
            
        finally:
            return bol_success
        
        
    def render(self, obj_state):
        """Line object to str"""
        
        str_out = ""
        #FIXME
        
        str_out += "%13.4f%8.4f" % (obj_line.freq, obj_line.freqErr)
        str_out += "%8.4f%2d"    % (obj_line.logI, obj_line.freedom)
        str_out += "%10.4f%3d%s" % (obj_line.Elow, obj_line.g, obj_line.tag)
        str_out += "".join(obj_line.qUpper) + "".join(obj_line.qLower) + " "
               
        return str_out
