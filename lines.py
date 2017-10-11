# python 2.7
#
# Version 1
#

# globals
MINUS = '-'

class Line:
    """A line entry object"""
    def __init__(self):
            self.valid = False
            
            # Frequency of the line (usually in MHz)
            self.freq      = None           
            self.freqErr   = None

            # base10 log of the integrated intensity at 300 K (in nm2MHz)
            self.logI      = None  
            self.freedom   = None
            
            # lower state energy (in cm-1), etc.
            self.Elow      = None       
            self.g         = None
            self.EinsteinA = None    
            self.tag       = None
            self.flag_lab  = None
            
            # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
            self.pressureAlpha = None    
            self.pressureDelta = None  
            
            # quantum numbers
            self.str_quanta = ""
            
            # egy file information
            self.hiblk   = None
            self.hindx   = None
            self.ElowErr = None
            self.pmix    = None
    
    def qn_upper(int_idx):
        """get upper quantum number u[int_idx] as str"""
        
        int_c = len(self.str_quanta) / 4
        int_s = int_idx * 2
         
        return self.str_quanta[int_s:int_s+2]
    
    
    def qn_lower(int_idx):
        """get lower quantum number l[int_idx] as str"""
        
        int_c = len(self.str_quanta) / 4
        int_s = (int_c + int_idx) * 2
         
        return self.str_quanta[int_s:int_s+2]
                        
                        
class CatConverter:
    """Manages entries of .cat files"""
    
    def get_str_quanta(str_line):
        """get the unque quanta of transition"""
        
        return str_line[55:79]
    
    
    def update_line(str_line, obj_line):
        """str to Line object (except quanta)"""
        
        try:
            flag_success = True
            
            obj_line.freq    = float(str_line[0:13])           
            obj_line.freqErr = float(str_line[13:21])

            obj_line.logI    = float(str_line[21:29]) 
            obj_line.freedom = int(str_line[29:31])
            
            obj_line.Elow    = float(str_line[31:41])       
            obj_line.g       = int(str_line[41:44])
            obj_line.tag     = str_line[44:55]
            
            obj_line.flagLab = (MINUS in obj_line.tagExt)
            
        except:
            flag_success = False
            
        finally:
            return flag_success
        
        
    def render_line(obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_out += "%13.4f%8.4f" % (obj_line.freq, obj_line.freqErr)
        str_out += "%8.4f%2d"    % (obj_line.logI, obj_line.freedom)
        str_out += "%10.4f%3d%s" % (obj_line.Elow, obj_line.g, obj_line.tag)
        str_out += "".join(obj_line.qUpper) + "".join(obj_line.qLower) + " "
               
        return str_out



class EgyConverter:
    """Manages entries of .egy files"""
    
    def get_str_quanta(str_line):
        """get the unque quanta of transition"""
        
        return str_line[55:79]
    
    
    def update_line(obj_line, str_line):
        """str to Line object (except quanta)"""
        
        try:
            flag_success = True

            obj_line.Elow    = float(str_line[31:41])       
            obj_line.ElowErr = float(str_line[41:44])
            
            obj_line.Elow    = float(str_line[31:41])       
            obj_line.ElowErr = float(str_line[41:44])
            obj_line.tag     = str_line[44:55]
            
            obj_line.flagLab = (MINUS in obj_line.tagExt)
            
            for i in range(0, 6): # max 6 quanta
                obj_line.qUpper.append(str_line[55 + i * 2 : 55 + i * 2 + 2])
                obj_line.qLower.append(str_line[67 + i * 2: 67 + i * 2 + 2])
                
            self.strLowerState = ','.join(self.qLower)
            self.strUpperState = ','.join(self.qUpper)
            
        except:
            flag_success = False
            
        finally:
            return flag_success
        
        
    def render_line(obj_line):
        """Line object to str"""
        
        str_out = ""
        
        str_out += "%13.4f%8.4f" % (obj_line.freq, obj_line.freqErr)
        str_out += "%8.4f%2d"    % (obj_line.logI, obj_line.freedom)
        str_out += "%10.4f%3d%s" % (obj_line.Elow, obj_line.g, obj_line.tag)
        str_out += "".join(obj_line.qUpper) + "".join(obj_line.qLower) + " "
               
        return str_out
