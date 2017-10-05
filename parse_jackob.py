#!/bin/python

from sys import argv as ARGV;
import numpy as np;
import h5py;

# settings
filenames = {};
filenames["input"] = "";
filenames["output_prefix"] = "data";
n_sideband = 1; # 1 - lower, 2 - upper, 3 - both

# input filename from ARGV
if len(ARGV) >= 2: 
	filenames["input"] = ARGV[1];

with h5py.File(filenames['input'], 'r') as f:
    keys = f.keys();
    for i in range(0, len(keys)):
        cold_mit = f[keys[i]]['level0']['COLD_MOL_0'][:];
        cold_ohne = f[keys[i]]['level0']['COLD_NO_MOL_0'][:];
        hot_ohne = f[keys[i]]['level0']['HOT_NO_MOL_0'][:];

        lfreq = f[keys[i]]['level1']['calibrated'][:,1]*1000;
        rfreq = f[keys[i]]['level1']['calibrated'][:,2]*1000;
        intensity = f[keys[i]]['level1']['calibrated'][:,3];
        
        if(n_sideband == 1):
            result = np.vstack([lfreq, intensity]).transpose();
        elif(n_sideband == 2):
            result = np.vstack([rfreq[::-1], intensity[::-1]]).transpose();
        elif(n_sideband == 3):
            result = np.vstack([lfreq, rfreq, intensity]).transpose();
       
        np.savetxt(filenames["output_prefix"] + str(i) + '.txt', result);