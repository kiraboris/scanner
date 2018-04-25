
folder = "/home/borisov/InSync/astro_cologne/work/VinylCyanide/"

peaklist = {}
with open(folder + "calc.txt", 'w') as f:
    for line in f:
        line = line.strip().split()
        
        peaklist[float(line[0])] = float(line[0])
        
        
def extract_peaks(peaklist, xxx, flag_area = False):
    
    calc_x    = np.linspace(xxx[0], xxx[-1], num = 2 * len(xxx))
    calc_y    = np.zeros(calc_x.shape)
    calc_ny_t = np.zeros(calc_x.shape)
    calc_ny   = np.zeros(calc_x.shape)
    
    for p in peaklist:
        index = bisect.bisect_left(calc_x, peak_maximum(p))
        
        if index <= 0 or index >= len(calc_x) - 1:
            continue
        
        calc_ny_t[index] += 1
        ny_i = calc_ny[index] + 1
        y_i  = calc_y[index] + peak_value(p, flag_area)
        
        if( calc_ny_t[index] >= calc_ny_t[index+1] 
            and calc_ny_t[index] >= calc_ny_t[index-1] ):
            di = 0
        elif( calc_ny_t[index+1] >= calc_ny_t[index] 
            and calc_ny_t[index+1] >= calc_ny_t[index-1] ):
            di = +1
        else:
            di = -1
            
        calc_y[index-1:index+2] = 0 
        calc_ny[index-1:index+2] = 0
        
        calc_y[index+di] = y_i
        calc_ny[index+di] = ny_i 
    
    for i in range(0, len(calc_x)):
        if calc_ny[i] > 0:
            calc_y[i] = calc_y[i] / calc_ny[i]
    
    return calc_x, calc_y

