
import numpy as np
from collections import defaultdict

from . import entities
from . import ranges
from . import peakfinder
from . import pickett
from . import simple_io
from .specunits import units

def peak_to_line(peak, factor):
    line = entities.Line()
    line.freq = peakfinder.peak_maximum(p) * factor
    line.freq_err = peakfinder.peak_fwhm(p) * factor
    line.log_I = np.log10( peak_value(p, flag_area=True) )
    return line 


class Experiment:

    def __init__(self, settings):
        self.settings = settings
        self.ranges = None
        self.lines = []
    
    def load_lines(self, filename, fileformat):
        
        if fileformat == 'simple':
            self.lines = simple_io.load_lines(filename)
        #elif fileformat == 'lin':
        #    self.lines = pickett.load_lin(filename) 
        elif fileformat == 'cat':
            self.lines = pickett.load_cat(filename) 
    
    def save_lines(self, filename, fileformat):
        
        if fileformat == 'lin':
            pickett.save_lin(filename, self.lines)
        elif fileformat == 'simple':
            simple_io.save_lines(filename, self.lines)
    
    def extract_peaks(self, threshold):
        
        peaklist = peakfinder.find_peaks(self.ranges, self.settings)
        
        factor = self.settings.data_units.to(units.MHz).magnitude
        
        lines = [peak_to_line(p, factor) for p in peaklist]
        
        self.lines = self.filter_lines(lines, threshold)

    def filter_lines(self, lines, threshold = 1.5):
       
        spacing = self.settings.min_fwhm.to(units.MHz).magnitude * 2

        new_lines = []
        accepted_index_to_count = {}
        min_log_I = abs(min(lines, key = lambda x: abs(x.log_I)).log_I)
        
        for i, i_line in enumerate(lines):
        
            if abs(i_line.log_I) > threshold + min_log_I:
                continue

            flag_found = False
            for k, k_line in enumerate(new_lines):
                if k_line.freq - spacing < i_line.freq < k_line.freq + spacing:
                    k_line.freq += i_line.freq
                    k_line.log_I = np.log10(10 ** k_line.log_I + 10 ** i_line.log_I)
                    accepted_index_to_count[k] += 1
                    flag_found = True
            
            if not flag_found:
                new_lines.append(i_line)
                accepted_index_to_count[len(new_lines)-1] = 1
            
        for k, k_line in enumerate(new_lines):
            k_line.freq /= accepted_index_to_count[k]
            k_line.log_I -= np.log10(accepted_index_to_count[k])

        return new_lines



