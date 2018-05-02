
from pickett import pickett

filename_test = "/home/borisov/projects/work/VinylCyanide/autofit_0/try1stage1.lin"
filename_cat = "/home/borisov/projects/work/VinylCyanide/c053515.cat"

fmt = pickett.get_quantum_fmt(filename_cat)
linelist_test = pickett.load_pgo_lin(filename_test, fmt)
linelist_cat = pickett.load_cat(filename_cat)


linelist_cat_dict = pickett.make_dict(linelist_cat)


def print_line(line, real_line):
    print("Frequency: {:.4f}, actual frequency {:.4f}".
          format(line.freq, line_real.freq), end='')

def criterium(line, real_line):
    return abs(line.freq - real_line.freq) < .100 # MHz

for line in linelist_test:
    if line.qid() in linelist_cat_dict:
        line_real = linelist_cat_dict[line.qid()]
        print_line(line, line_real)
        if not criterium(line, line_real):    
            print(" --> mismatch!")
        else:
            print(" --> ok")
        
