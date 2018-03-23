# python 2,3
#
# Functions for User <-> Knowledge interaction
#

import inspect

class SourceDB:
    
    def __init__(self, modulename, flag_autosave=True):
        
        self.__db = __import__(modulename)
        self.__filename = inspect.getfile(self.__db)
        self.__autosave = flag_autosave
        self.__observed_names = set()
    
    
    def save(self):
        
        self.__savebuf(self.__update_blocks(self.__loadbuf()))
    
    
    def __loadbuf(self):

        with open(self.__filename, 'r') as me:
            buf = me.readlines()
        
        return buf            
    
    
    def __savebuf(self, buf):

        with open(self.__filename, 'w') as me:
            me.writelines(buf)
    
    
    def __update_blocks(self, buf):
        
        for name in self.__observed_names:
            buf = self.__update_block(buf, name)     
        
        return buf
    
    
    def __update_block(self, buf, name):
        
        start_i, end_i = self.__find_block(buf, name)
        
        return buf[:start_i] + [self.__make_block(name)] + buf[end_i+1:]
    
    def __make_block(self, name):
        
        title = name + ' = '
        
        replacement = ',\n' + ' ' * len(title) 
        
        return title + repr(self.__get(name)).replace(',', replacement) + '\n'
   
   
    def  __find_block(self, buf, name):
        
        for cur_i, line in enumerate(buf):
            if name in line:
                start_i = cur_i
        
        for cur_i in range(start_i, len(buf)):    
            if self.__is_matched("\n".join(buf[start_i:cur_i+1])):
                end_i = cur_i
                break
                
        return start_i, end_i
    
    
    def __is_matched(self, expression):
        
        opening = '({['
        closing = ')}]'
        mapping = dict(zip(opening, closing))
        queue = []

        for letter in expression:
            if letter in opening:
                queue.append(mapping[letter]) 
            elif letter in closing:
                if not queue or letter != queue.pop():
                    return False
                    
        return not queue
            
    
    def __get(self, key):
        
        return vars(self.__db)[key]
    
        
    def __getattr__(self, key):
        
        self.__observed_names.add(key)
        
        return self.__get(key)  

                    
                    
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
    
    
    
    
