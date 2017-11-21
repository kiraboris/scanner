#!/bin/python
# python 2.4
import numpy as np
import begin

def interpolate(x1, y1, x2, y2, x):
	assert(x >= x1 and x2 >= x and x2 > x1)
	y = y1 + (y2 - y1) / (x2 - x1) * (x - x1);
	return y

def match_data(data): 
	# data must be a list of 2-columned arrays
	datasets = [ a[a[:, 0].argsort()] for a in data ]
	
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
		for j in range(len(trav)):  

			while(datasets[j][trav[j], 0] < x_i):
				trav[j] = trav[j] + 1
			
			x_t_j = datasets[j][trav[j], 0]
			y_t_j = datasets[j][trav[j], -1]
			
			if(x_t_j == x_i):
				yvalues[i, j] = y_t_j
			else:  # only x_t_j > x with trav[j] > 0 	 
				x_t_j_minus = datasets[j][trav[j]-1, 0]
				y_t_j_minus = datasets[j][trav[j]-1, -1]

				yvalues[i, j] = interpolate(x_t_j_minus, y_t_j_minus, x_t_j, y_t_j, x_i)
				
	out = np.column_stack((xvalues, yvalues))
	return out

@begin.start
def main(output="out.txt", *files):
	"""Matches multiple (x,y) datasets into one. Assumption: continuous common x range exists, x data are sorted ascending. All x point inside common range are preserved."""
	
	# read
	in_data = []   
	for filename in files: 
		in_data.append(np.loadtxt(filename))
	
	out_data = match_data(in_data)
	
	# write
	np.savetxt(output, out_data)


