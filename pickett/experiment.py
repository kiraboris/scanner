
import numpy as np
from collections import defaultdict

from . import entities
from . import ranges
from . import peakfinder
from . import pickett
from .units import units

def peak_to_line(peak, factor):
    line = Line()
    line.freq = peakfinder.peak_maximum(p) * factor
    line.freq_err = peakfinder.peak_fwhm(p) * factor
    line.log_I = np.log10( peak_value(p, flag_area=True) )
    return line 

def load_simple_format(filename):
    
    lines = []
    with open(filename, 'r') as f:
        for s in f:
            s = s.strip().split()
            
            line = Line()
            line.freq = float(s[0])
            line.log_I = float(s[1])
            
            lines.append(line)
            
    return lines


class Experiment:

    def __init__(self, settings):
        self.settings = settings
        self.ranges = None
        self.lines = []
    
    def load_lines(self, filename, flag_simple_format_dump = False):
        
        if flag_simple_format_dump:
            self.lines = self.filter_lines(load_simple_format(filename))
        else:
            self.lines = pickett.load_lin(filename) 
    
    def save_lines(self, filename):
        
        pickett.save_lin(self.lines, filename)
    
    def extract_peaks(self):
        
        peaklist = peakfinder.find_peaks(self.ranges, self.settings)
        
        factor = self.settings.data_units.to(units.MHz).magnitude
        
        lines = [peak_to_line(p, factor) for p in peaklist]
        
        self.lines = self.filter_lines(lines)

    def filter_lines(self, lines, threshold = 0.8):
       
        spacing = settings.min_fwhm.to(units.MHz).magnitude
        
        new_lines = []
        accepted_index_to_count = defaultdict(int)
        max_logI = max(lines, key = lambda x: x.logI)
        
        for i, i_line in enumerate(lines):
        
            if line.logI < threshold * max_logI:
                continue
            
            for k, k_line in enumerate(new_lines):
                if k_line.freq - spacing < i_line.freq < k_line.freq + spacing:
                    k_line.freq += i_line.freq
                    k_line.log_I += np.log10(10 ** k_line.log_I + 10 ** i_line.log_I)
                    accepted_index_to_count[k] += 1
                else:
                    new_lines.append(i_line)
                    accepted_index_to_count[len(new_lines)-1] = 1
            
        for k, k_line in enumerate(new_lines):
            k_line.freq /= accepted_index_to_count[i]
            k_line.log_I -= np.log10(accepted_index_to_count[i])

        return new_lines

