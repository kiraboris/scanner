#  **** pickett knowledge base ****

from bidict import bidict

PARAM_CODES = bidict({'-DJK': 1100,
               '-DJ': 200,
               'A': 10000,
               '-DK': 2000,
               'B': 20000,
               'C': 30000})


INVERSE_PARAMS = ['DJ',
                  'DK',
                  'DJK']
                               
QUANTA_HEADERS = {2: ['N',
                  'K',
                  'J',
                  'F1',
                  'F2',
                  'F'],
                  13: ['N',
                  'K',
                  'v',
                  'J',
                  'F1',
                  'F']}

