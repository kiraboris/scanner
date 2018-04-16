
import pint


class Units:

    @staticmethod
    def prefixes():
        return [
            'yocto- = 1e-24 = y-',
            'zepto- = 1e-21 = z-',
            'atto- =  1e-18 = a-',
            'femto- = 1e-15 = f-',
            'pico- =  1e-12 = p-',
            'nano- =  1e-9  = n-',
            'micro- = 1e-6  = u-',
            'milli- = 1e-3  = m-',
            'centi- = 1e-2  = c-',
            'deci- =  1e-1  = d-',
            'deca- =  1e+1  = da- = deka',
            'hecto- = 1e2   = h-',
            'kilo- =  1e3   = k-',
            'mega- =  1e6   = M-',
            'giga- =  1e9   = G-',
            'tera- =  1e12  = T-',
            'peta- =  1e15  = P-',
            'exa- =   1e18  = E-',
            'zetta- = 1e21  = Z-',
            'yotta- = 1e24  = Y-'
        ]

    @staticmethod
    def spec_units():
        lst_units = ([
                         'second = [time] = s',
                         'hertz = 1 / s = Hz',
                         'meter = s / 299792458 = m',
                         'wavenumber = 1 / cm = wn',
                     ]
                     + Units.prefixes())

        units = pint.UnitRegistry(None)
        units.load_definitions(lst_units)

        return units
