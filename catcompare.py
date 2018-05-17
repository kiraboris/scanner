
from pickett import pickett

def print_line(line, real_line):
    print("Frequency: {:.4f}, actual frequency {:.4f}".
          format(line.freq, real_line.freq), end='')

def criterium(line, real_line):
    return abs(line.freq - real_line.freq) < 1.500 # MHz


def compare(filename_test, filename_cat):
    
    fmt = pickett.get_quantum_fmt(filename_cat)
    linelist_test = pickett.load_pgo_lin(filename_test, fmt)
    linelist_cat = pickett.load_cat(filename_cat)
    linelist_cat_dict = pickett.make_dict(linelist_cat)
      
    for line in linelist_test:
        if line.qid() in linelist_cat_dict:
            line_real = linelist_cat_dict[line.qid()]
            print_line(line, line_real)
            if not criterium(line, line_real):    
                print(" --> mismatch!")
            else:
                print(" --> ok")
        

filename_test = "/home/borisov/InSync/astro_cologne/work/VinylCyanide/autofit_1/try2stage2a.lin"
filename_cat = "/home/borisov/InSync/astro_cologne/work/VinylCyanide/c053515.cat"
compare(filename_test, filename_cat)
