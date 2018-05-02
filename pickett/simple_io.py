
from . import entities

def load_lines(filename):
    
    lines = []
    with open(filename, 'r') as f:
        for s in f:
            s = s.strip().split()
            
            line = entities.Line()
            line.freq = float(s[0])
            line.log_I = float(s[1])
            
            lines.append(line)
            
    return lines

def save_lines(filename, lines):

    with open(filename, 'w') as f:
        for line in lines:
            freq = line.freq
            intens = line.log_I
            f.write("{}\t{}\n".format(freq, intens))
