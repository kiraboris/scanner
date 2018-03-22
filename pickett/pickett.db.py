#  **** pickett knowledge base ****

PARAM_CODES = bidict({
    'A': 10000,
    'B': 20000,
    'C': 30000,
    '-DJ': 200,
    '-DK': 2000,
    '-DJK': 1100
    })

INVERSE_PARAMS = [
    'DJ',
    'DK', 
    'DJK'
    ]

QUANTA_HEADERS = {
    2:  ['N', 'K', 'J', 'F1', 'F2', 'F'],
    13: ['N', 'K', 'v', 'J', 'F1', 'F']
    }
