# python 2,3
#
# This is a self-upgrading knowledge base of pypickett
#

import inspect

def open_myself(flag):
    
    return open(inspect.getfile(__name__), flag)
    

#  **** pickett rotor parameters ****

KNOWN_PARAM_CODES = bidict({
    'A': 10000,
    'B': 20000,
    'C': 30000,
    '-DJ': 200,
    '-DK': 2000,
    '-DJK': 1100
    })
    

KNOWN_INVERSE_PARAMS = [
    'DJ',
    'DK', 
    'DJK'
    ]

def param_code(name):
    
    if name in KNOWN_INVERSE_PARAMS:
        name = '-' + name
    
    code = KNOWN_PARAM_CODES.get(name, 0)
    
    if code == 0:
        
        code = int(raw_input('Sorry, what is the code for %s? ' % name))
        
        KNOWN_PARAM_CODES[name] = code
        with open_myself('r') as me:
            buf = me.readlines()
            
        with open_myself('w') as me:
            for line in buf:
                me.write(line)
                if 'KNOWN_PARAM_CODES' in line:
                    me.write("'%s': %i,\n" % (name, code))
                
                if 'KNOWN_INVERSE_PARAMS' in line and '-' in name:
                    me.write("'%s',\n" % name)
                
    return code

# **** / pickett rotor parameters *****
