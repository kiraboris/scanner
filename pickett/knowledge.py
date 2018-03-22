# python 2,3
#
# Functions for User <-> Knowledge interaction
#

import inspect

class PyDB:
    
    def __init__(self, filename=None, modulename=None):
        
        if filename is None:
            if modulename is None:
                return
            else:
                filename = inspect.getfile(modulename).replace('.py', '.db.py')
        
        self.__filename = filename
        __import__(filename)
        
    def open(flag):
        """
            opens source code of module currenly being executed
        """
        return open(self.__filename, flag)
    
    def add(after_what_line, line_to_write):
        """
            adds a line_to_write to source code of module currenly being executed
            after known line_after (e.g. line containing certain variable name
        """
                
        with open('r') as me:
            buf = me.readlines()
            
        with opendb('w') as me:
            for line in buf:
                me.write(line)
                if after_what_line in line:
                    me.write("%s\n" % line_to_write)
                    
                    
def ask(text="", **kwargs):
    """
        may be custom input method
    """
    
    try:
        result = raw_input(text, **kwargs)
    except:
        result = input(text, **kwargs)
        
    return result


def say(text="", **kwargs):
    """
        may be custom output method
    """
    
    print(text, **kwargs)
    
