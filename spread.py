# python 2.4
import numpy as np

import match
import peakutils

#obs_files = ["data0.txt", "data1.txt", "data2.txt"];  
#alc_file = "ASCIIdata.LM.out.dat"
#output_file = "peaker_output.txt";


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

#data_mean = np.empty([len(data), 2])
#data_mean[:, 0] = data[:, 0]
#data_mean[:, 1] = np.mean(data[:, 2:], axis=1)
#np.savetxt('data_mean.txt', data_mean)
#exit()

xxx = data[:, 0] # 0th dataset are x-es
minimal_linewidth = 2  # at least 2 channels wide


# determine minimal linehights # TODO: find a smarter way
minimal_lineheights = []
noise_levels = []
for d in data[:, 1:].transpose():
	y_std   = np.std(d)
	y_max = max(abs(d))
	minimal_lineheights.append(y_std / y_max)
	noise_levels.append(y_std)

print "--Input--"
print "Assumed noise levels [K]:", [float("%0.2f" % x) for x in noise_levels]
print "Assumed least peakwidth :", minimal_linewidth, 'channels'

# find exp AND model peaks
peak_index_sets = []
for (d, t) in zip(data[:, 1:].transpose(), minimal_lineheights): 
	peak_index_sets.append(set(peakutils.indexes(d, thres = t, 
						min_dist = minimal_linewidth)))
							
peak_indexes = list(reduce(set.union, peak_index_sets))

# generate simplified datasets
data_simple = np.copy(data)
for d in data_simple[:, 1:].transpose(): 
	chi = np.zeros(len(d))
	chi[peak_indexes] = 1
	d[:] = d * chi
	

# find intersection of peak list, accounting for linewidth
# 'flatten' broad peaks
delta = minimal_linewidth * 2
peak_indexes_common =  []
for peak_pos in peak_indexes:
	flag = True
	for (st, d) in zip(peak_index_sets, data_simple[:, 1:].transpose()):
		span = [peak_pos + i for i in range(-delta, delta)]
		flag = flag & any([x in st for x in span])
		d[span] = max(d[span])
	if flag:
		peak_indexes_common.append(peak_pos)	
		
common_peaks_selector = np.in1d(peak_indexes, peak_indexes_common)		
#print sorted(peak_indexes_common)
#print sorted(peak_indexes)


# determine obsCv
d_mean = np.mean(data_simple[peak_indexes, 2:], axis = 1)
d_std  = np.std(data_simple[peak_indexes, 2:], axis = 1)
expCv  = d_std / d_mean 	 						

# determine (obsMu-calc)/obsMu
dev = (d_mean - data_simple[peak_indexes, 1]) / d_mean



#data_stat=np.zeros([len(data), 3])
#data_stat[:, 0] = data[:, 0]

peak_indexes_new = []
for (m, p) in zip(d_mean, peak_indexes):
	if m < 20 and data[p, 0] > 330600:
		pass
	else:
		peak_indexes_new.append(p)
		
		

filt = [p in peak_indexes_new for p in peak_indexes]


print 'Abweichungen: ' max(d_mean[filt]), 


#data_stat[peak_indexes_new, 1] = d_mean[filt]
#data_stat[peak_indexes_new, 2] = d_std[filt] / np.sqrt(3)



#np.savetxt('statisic.txt', data_stat)


exit()

							
# make plots
import matplotlib
matplotlib.use("qt5agg")
import matplotlib.pyplot as pl
import matplotlib.gridspec as plgs

fontsize = 16

f1 = pl.figure()

ax1 = f1.add_subplot(111)
ax1.set_xlabel("Frequency [GHz]", fontsize=fontsize)
ax1.tick_params(labelsize=fontsize-3)
yyy = np.zeros(len(xxx))
yyy[peak_indexes_common] =  expCv[common_peaks_selector]
ax1.plot(xxx / 1000, yyy * 100, 'g-', lw = 2)
#yyy = np.zeros(len(xxx))
#yyy[peak_indexes_common] =  dev[common_peaks_selector]
#ax1.plot((xxx + 2) / 1000, yyy * 100, 'c-', alpha=0.8, lw=2)
#ax1.legend(['$\sigma_{obs}\ \slash\ \mu_{obs}$', '$[\mu_{obs}\ -\ calc]\ \slash\ \mu_{obs}$'])
ax1.legend(['$\sigma_{obs}\ \slash\ \mu_{obs}$'])

ax1.tick_params(direction = 'in')
#ax1.grid()

f1.canvas.draw()  # !!
ylabels = [item.get_text() + "%" for item in ax1.get_yticklabels()]
ax1.set_yticklabels(ylabels)

f2=pl.figure()
gs = plgs.GridSpec(2, 1, height_ratios=[2, 1])
ax2 = f2.add_subplot(gs[0])
#ax2.set_xlabel("Frequency [GHz]", fontsize=fontsize)
ax2.set_ylabel("Intensity [K]", fontsize=fontsize)
ax2.tick_params(labelsize=fontsize-3)
#ax2.plot((xxx)/ 1000, np.mean(data[:, 2:], axis=1), 'b-')
ax2.plot((xxx)/ 1000, data[:, 4], 'b-')


ax2.plot((xxx + 2)/ 1000, data[:, 1], 'r-', alpha=0.8)
ax2.legend(['${obs}$', '$calc$'])
ax2.tick_params(direction = 'in')
ax3 = f2.add_subplot(gs[1])
#ax3.plot((xxx)/ 1000, np.mean(data[:, 2:], axis=1) - data[:, 1], 'k-')
ax3.plot((xxx)/ 1000, data[:, 4] - data[:, 1], 'k-')

ax3.legend(['${obs} - calc$'])
ax3.set_xlabel("Frequency [GHz]", fontsize=fontsize)
ax3.set_ylabel("Difference [K]", fontsize=fontsize)
ax3.tick_params(direction = 'in')



#f3=pl.figure()
#ax = f3.add_subplot(111)
#ax2.set_xlabel("Frequency [GHz]", fontsize=fontsize)
#ax2.set_ylabel("Intensity [K]", fontsize=fontsize)
#ax2.tick_params(labelsize=fontsize-3)
#ax.plot((xxx)/ 1000, data[:, 2], 'r-')
#ax.plot((xxx)/ 1000, data[:, 3], 'b-')
#ax.plot((xxx)/ 1000, data[:, 4], 'g-')

#ax2.legend(['$\mu_{obs}$', '$calc$'])
#ax2.tick_params(direction = 'in')
#ax3 = f2.add_subplot(gs[1])
#ax3.plot((xxx)/ 1000, np.mean(data[:, 2:], axis=1) - data[:, 1], 'k-')
#ax3.legend(['$\mu_{obs} - calc$'])
#ax3.set_xlabel("Frequency [GHz]", fontsize=fontsize)
#ax3.set_ylabel("Difference [K]", fontsize=fontsize)
#ax3.tick_params(direction = 'in')










#ax2.grid()

# print statistics
print "--Statistics--"
print "obsCv for union: "
print "  min %0.1f%%" % (min(expCv) * 100)
print "  max %0.1f%%" % (max(expCv) * 100)
print "  avg %0.1f%%" % (np.mean(expCv) * 100)
print 
print "obsCv for intersection: "
print "  min %0.1f%%" % (min(expCv[common_peaks_selector]) * 100)
print "  max %0.1f%%" % (max(expCv[common_peaks_selector]) * 100)
print "  avg %0.1f%%" % (np.mean(expCv[common_peaks_selector]) * 100)
print 
print "(obsMu-calc/obsMu) for union: "
print "  min %0.1f%%" % (min(abs(dev)) * 100)
print "  max %0.1f%%" % (max(abs(dev)) * 100)
print "  avg %0.1f%%" % (np.mean(abs(dev)) * 100)
print 
print "(obsMu-calc/obsMu) for intersection: "
print "  min %0.1f%%" % (min(abs(dev[common_peaks_selector])) * 100)
print "  max %0.1f%%" % (max(abs(dev[common_peaks_selector])) * 100)
print "  avg %0.1f%%" % (np.mean(abs(dev[common_peaks_selector])) * 100)


pl.show()
