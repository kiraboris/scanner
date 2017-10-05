# python 2.4
import numpy as np;

# settings
filenames = {};
filenames["expdata"] = "data_lim1015_scaled.txt";
filenames["modeldata"] = "xclass_spectrum_output_293K.dat";
filenames["output"] = "data_combined2.txt";

# read
exp = np.loadtxt(filenames["expdata"]);
model = np.loadtxt(filenames["modeldata"]);

FREQ = 0;
jlen = model.shape[0];
ilen = exp.shape[0];
out = np.empty([ilen, 3]);
   
# ** main part **

# write
np.savetxt(filenames["output"], out);
     
#EOF