
from pickett import pickett

filename_test = "/home/borisov/projects/work/VinylCyanide/autofit_0/try2stage2b.lin"
filename_cat = "/home/borisov/projects/work/VinylCyanide/c053515.cat"

fmt = pickett.get_quantum_fmt(filename_cat)
linelist_test = pickett.load_pgo_lin(filename_test, fmt)
linelist_cat = pickett.load_cat(filename_cat)


linelist_cat_dict = pickett.make_dict(linelist_cat)


def print_line_beginning(line, real_line):
    print("Frequency: {:.4f}, actual frequency {:.4f}".
          format(line.freq, line_real.freq), end='')

def print_criterium(line, real_line, max_delta):
    if abs(line.freq - real_line.freq) <= max_delta:
        print(" --> ok (delta = {:.3f} <= {:.3f})".
                  format(abs(line.freq - line_real.freq), max_delta),  end='')
    else:
        print(" --> mismatch! (delta = {:.3f} > {:.3f})".
                  format(abs(line.freq - line_real.freq), max_delta),  end='')

max_delta = 0.100 #MHz
for line in linelist_test:
    if line.qid() in linelist_cat_dict:
        line_real = linelist_cat_dict[line.qid()]
        print_line_beginning(line, line_real)
        print_criterium(line, line_real, max_delta)
        print('')

            
        
