# python 2.7


class Line:
    """A line entry object"""
    def __init__(self):
            line.valid = False
            
            # Frequency of the line (usually in MHz)
            line.freq      = None           
            line.freqErr   = None

            # base10 log of the integrated intensity at 300 K (in nm2MHz)
            line.logI      = None  
            
            # lower state energy (in cm-1), etc.
            line.Elow      = None       
            line.g         = None
            self.EinsteinA = None     
            
            # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
            self.pressureAlpha = None    
            self.pressureDelta = None  
            
            # quantum numbers
            self.qUpper = []
            self.qLower = []
            self.strLowerState = ""
            self.strUpperState = ""
    
    
class CatConverter:
    """Manages entries of .cat files"""
    
    def parse(str_line, obj_line):
        """str to Line object"""
        
        line = Line()
        try:
            line.valid = True
            
            obj_line.freq    = float(str_line[0:13])           
            obj_line.freqErr = float(str_line[13:21])

            obj_line.logI    = float(str_line[21:29]) 
            obj_line.flagOne = str_line[29:31]
            
            obj_line.Elow    = float(str_line[31:41])       
            obj_line.g       = int(str_line[41:44])
            obj_line.flagTwo = str_line[44:55]
            
            for i in range(0, 6):
                obj_line.qUpper.append(str_line[55 + i * 2 : 55 + i * 2 + 2])
                obj_line.qLower.append(str_line[67 + i * 2: 67 + i * 2 + 2])
                
            self.strLowerState = ','.join(self.qLower)
            self.strUpperState = ','.join(self.qUpper)
            
        except:
            self.valid = False
        
        
        
    def render(obj_line):
        """Line object to str"""
        
        

class EgyConverter:
    """Converts string entries of .egy file to a dict, and vice versa."""
