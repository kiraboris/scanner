# python 2.4
import numpy as np;
import peakutils;
import math;

# convention: data[:,0]- frequency, data[:,1] - obs, data[:, 2] - calc

# settings
filenames = {};
filenames["data"] =   "data_combined.txt";
filenames["output"] = "peak_deviations_percent.txt";
minimal_linewidth = 0.4; #MHz
minimal_lineheight = 3.5; #K

# read
data = np.loadtxt(filenames["data"]);
out = np.zeros([data.shape[0],2]);
out[:, 0:1] = data[:, 0:1]
   
# main part
minimal_linewidth_samples = int(
    data.shape[0] / (abs(data[-1,0] - data[0,0])) * minimal_linewidth);
minimal_lineheight_normalized = minimal_lineheight / max(data[:,2]);
peak_indexes = peakutils.indexes(
    data[:,2], thres = minimal_lineheight_normalized, min_dist = minimal_linewidth_samples);
# TODO: find also peaks for data[:,1] and cover case if peaks dont't match exactly, 
#  but lie in minimal_linewidth


print("Peaks found: " + str(len(peak_indexes)));
print("Max deviation: " + str(max(abs(out[:,1]))) + "%");  
    
for i in peak_indexes:
    out[i,1] = (data[i,1] - data[i, 2]) / data[i, 1] * 100;

# write
np.savetxt(filenames["output"], out);
