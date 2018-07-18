
import numpy as np
from . import entities


def load_lines(filename):
    lines = []
    with open(filename, 'r') as f:
        for s in f:
            s = s.strip().split()
            
            line = entities.Line()
            
            if len(s) == 2:
                line.freq = float(s[0])
                line.log_I = np.log10(float(s[1]))
            elif len(s) == 3:
                line.freq = float(s[0])
                line.freq_err = float(s[1])
                line.log_I = float(s[2])
            
            lines.append(line)
            
    return lines


def save_lines(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            freq = line.freq
            intens = 10 ** line.log_I
            f.write("{}\t{}\n".format(freq, intens))
