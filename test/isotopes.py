
import numpy as np
from pickett_old import pickett

# Isotope ratios
C12 = 0.9893
C13 = 0.0107

O16 = 0.9976
O17 = 0.0004
O18 = 0.0020

S32 = 0.9499
S33 = 0.0075
S34 = 0.0425

spec_list = [('c060503', O16 * C12 * S32), ('c060504', O16 * C12 * S32), ('c061502', O16 * C13 * S32),
             ('c061503', O16 * C12 * S33), ('c061504', O17 * C12 * S32), ('c062505', O16 * C12 * S34),
             ('c062506', O18 * C12 * S32), ('c062507', O16 * C13 * S33)]

folder = "C:\\Users\\Kirill\\Dropbox\\astro_cologne\\work\\OCS\\"


def change_instensity(templist, factor):
    for line in templist:
        line.log_I += np.log10(factor)

linelist = []
for spec in spec_list:
    templist = pickett.load_cat(folder + spec[0] + '.cat')
    change_instensity(templist, spec[1])
    linelist += templist

pickett.save_cat(folder + 'out.cat', linelist)
