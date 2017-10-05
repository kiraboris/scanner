#!/bin/python
# python 2.4
import numpy as np;
import sys
#import matplotlib.pyplot as pl;

def main():
	# settings
	filenames = {};
	filenames["output"] = "data_combined2.txt"

	# input filenames
	if len(sys.argv) < 3: 
		filenames["expdata"] = raw_input("Enter expdata filename, please: ")
		filenames["modeldata"] = raw_input("Enter modeldata filename, please: ")
	else:
		filenames["expdata"]  = sys.argv[1]
		filenames["modeldata"]  = sys.argv[2]

	# read
	# assumption: frequencies sorted ascending
	exp = np.loadtxt(filenames["expdata"])
	model = np.loadtxt(filenames["modeldata"])
	
	out = match([exp, model])
	
	# write
	np.savetxt(filenames["output"], out)	

def interpolate(x1, y1, x2, y2, x):
    assert(x >= x1 and x2 >= x and x2 > x1)
    y = y1 + (y2 - y1) / (x2 - x1) * (x - x1);
    return y

def match(data): 
	# data must be a list of 2-columned arrays
	datasets = [ a[a[:, 0].argsort()] for a in data ]
	
	#pl.plot(datasets[0][:,0], datasets[0][:,1]);
	#pl.plot(modeldata[:,0], modeldata[:,1]);
	#pl.show();
			
	xl = max([ a[ 0, 0] for a in datasets ])
	xh = min([ a[-1, 0] for a in datasets ])
	assert(xh >= xl)  # ensure common range is found 
	
	set_xvalues = set()
	for a in datasets:
		for x in a[:, 0]:
			if(x >= xl and x <= xh):
				set_xvalues.add(x)

	xvalues = list(set_xvalues)
	xvalues.sort()
	yvalues = np.empty((len(xvalues), len(datasets)))
	trav = [0] * len(datasets) 
	
	for (i, x_i) in enumerate(xvalues): 
		#print trav        
		#_S= raw_input()         
		for j in range(len(trav)):  

			while(datasets[j][trav[j], 0] < x_i):
				trav[j] = trav[j] + 1
			
			x_t_j = datasets[j][trav[j], 0]
			y_t_j = datasets[j][trav[j], 1]
			
			#if y_t_j > 10.0:
			#	print i
				
				
				
			if(x_t_j == x_i):
				yvalues[i, j] = y_t_j
			else:  # only x_t_j > x with trav[j] > 0 	 
				x_t_j_minus = datasets[j][trav[j]-1, 0]
				y_t_j_minus = datasets[j][trav[j]-1, 1]
			#	if(j == 0 and y_t_j > 10.0):
			#		print x_i, x_t_j_minus, x_t_j, y_t_j_minus, y_t_j
			#		_S= raw_input() 
				yvalues[i, j] = interpolate(x_t_j_minus, y_t_j_minus, x_t_j, y_t_j, x_i)
				
	out = np.column_stack((xvalues, yvalues))
 	return out

	if(__name__ == '__main__'):  
		main()
