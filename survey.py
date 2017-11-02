#!/bin/python
# python 2.4
import numpy as np
import begin

def interpolate(x1, y1, x2, y2, x):
	assert(x >= x1 and x2 >= x and x2 > x1)
	y = y1 + (y2 - y1) / (x2 - x1) * (x - x1);
	return y

def stack_data(data): 
	# data must be a list of 2-columned arrays
	datasets = [ a[a[:, 0].argsort()] for a in data ]
	
	set_xvalues = set()
	for a in datasets:
		for x in a[:, 0]:
			set_xvalues.add(x)

	xvalues = list(set_xvalues)
	xvalues.sort()
	yvalues = np.empty((len(xvalues), 1))
	trav = [0] * len(datasets) 
	
	for (i, x_i) in enumerate(xvalues): 
 		yvals_local = []   
		for j in range(len(trav)):  
			
			x_t = datasets[j][:, 0]
			y_t = datasets[j][:, -1]
			
			if (x_t[0] > x_i) or (x_t[-1] < x_i):
				continue 
			
			while(x_t[trav[j]] < x_i):
				trav[j] = trav[j] + 1
			
			x_t_j = x_t[trav[j]]
			y_t_j = y_t[trav[j]]
			
			#print [x_t[trav[j]-1], x_i, x_t_j] 
			if(x_t_j == x_i):
				yvals_local.append(y_t_j)
			else:  # only x_t_j > x_i with trav[j] > 0 
				x_t_j_minus = x_t[trav[j]-1]
				y_t_j_minus = y_t[trav[j]-1]
				
				yvals_local.append(interpolate(x_t_j_minus, y_t_j_minus, x_t_j, y_t_j, x_i))
			
		yvalues[i] = max(yvals_local)             
				
	out = np.column_stack((xvalues*1000, yvalues))
	return out

@begin.start
def main(output="out.txt", *files):
	"""Stacks multiple (x,y) datasets into one. Interpolates and averages datapoints in x ranges which several datasets share. Assumption: x data are sorted ascending. All x point inside common ranges are preserved."""
	
	# read
	in_data = []   
	for filename in files: 
		in_data.append(np.loadtxt(filename))
	
	out_data = stack_data(in_data)
	
	# write
	np.savetxt(output, out_data)


