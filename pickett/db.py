
from bidict import bidict

PARAM_CODES = bidict({'DJK': 1100,
                      'DJ': 200,
                      'A': 10000,
                      'DK': 2000,
                      'B': 20000,
                      'C': 30000})


QUANTA_HEADERS = {2: ['N', 'K', 'J', 'F1', 'F2','F'],
                  3: ['N', 'Ka', 'Kc', 'v', 'J', 'F'],
                  13: ['N', 'K', 'v', 'J', 'F1', 'F'],
                  14: ['N', 'Ka', 'Kc', 'v', 'J', 'F']}

MODEL_EXTENSIONS = [".par", ".var", ".int"]

def strip_possible_param_inversion(name):

    if name[0] == '-':
        return name[1:]
    else:
        return name


def param_code(name):
    name = strip_possible_param_inversion(name)

    return PARAM_CODES[name]


def quanta_headers(int_fmt):
    """returns list of quantum number names for a Pickett code"""

    int_c = int_fmt % 10
    int_Q = int_fmt // 100

    return QUANTA_HEADERS[int_Q][0:int_c]
