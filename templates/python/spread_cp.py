# python 2.4
import numpy as np
import matplotlib.pyplot as pl;

import match
import peakutils

#obs_files = ["data0.txt", "data1.txt", "data2.txt"];  
#alc_file = "ASCIIdata.LM.out.dat"
#output_file = "peaker_output.txt";

# TODO: determine these things automatically
#minimal_linewidth = 0.4;  # MHz
#minimal_lineheight = 10;  # percent

#out = np.empty([data.shape[0],2]);
#out[:, 0:1] = data[:, 0:1]

#np.savetxt(output_file, out);

#modeldata   = np.loadtxt(calc_file)
#expdata = [np.loadtxt(name) for name in obs_files]
#alldata = [modeldata] + expdata

#data = match.match(alldata)

#np.savetxt('data_combined.txt', data);

data = np.loadtxt('data_combined.txt')

x = data[:, 0] # 0th dataset are x-es
minimal_linewidth_samples = 2  # at least 2 channels wide

# determine minimal linehights
minimal_lineheights = []
noise_levels = []
for d in data[:, 1:].transpose():
	#print d.shape
	thres_l = 0.0
	thres_h = 1.0
	while True:
		thres = (thres_h + thres_l) / 2
		y_thres = max(abs(d)) * thres
		y_m     = np.mean(d[abs(d) <= y_thres])
		y_std   = np.std(d[abs(d) <= y_thres])
		y_m_std = y_std / np.sqrt(len(d[abs(d) <= y_thres]))
		
		#print y_mean,y_std
		if np.sign(y_m - 20 * y_m_std) != np.sign(y_m + 20 * y_m_std):
			thres_l = thres
		else:
			thres_h = thres
			
		print 	thres,	thres_h , thres_l, y_m, y_m_std
		if 	thres_h - thres_l < 0.001:
			minimal_lineheights.append(thres)
			noise_levels.append(max(abs(d)) * thres)
			break

print "Noise levels [K]:", noise_levels
print "Noise levels [K]:", minimal_lineheights
exit()

# find exp peaks
peak_index_lists = []
for d in data[:, 2:].transpose(): # 1th dataset are model data
	peak_index_lists.append(peakutils.indexes(d, 
						thres = minimal_lineheight / 100.0, 
						min_dist = minimal_linewidth_samples))
							
peak_indexes = list(set(np.concatenate(peak_index_lists)))

# determine exp Cv
for d in data[:, 2:].transpose(): # 1th dataset are model data 
	chi = np.zeros(len(d))
	chi[peak_indexes] = 1
	d[:] = d * chi

d_mean = np.mean(data[peak_indexes, 1:-1], axis = 1)
d_std  = np.std(data[peak_indexes, 1:-1], axis = 1)
expCv  = d_std / d_mean 	 						

# find model peaks


# make plots
y = data[:, 3]
y = np.zeros(len(x))
y[peak_indexes] =  Cv

pl.plot(x, y)
pl.show();

