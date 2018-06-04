
from pickett import pickett

def signum(line):
    if line.int_cat_tag > 0:
        return " "
    else:
        return "+"

def print_line(line, real_line):
    print("Frequency: {:.4f}, actual frequency {}{:.4f}".
          format(line.freq, signum(real_line), real_line.freq), end='')

def criterium(line, real_line):
    return abs(line.freq - real_line.freq) < 1.000 # MHz


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
        

filename_test = "/home/borisov/Dropbox/astro_cologne/work/VinylCyanide/autofit_1/try4stage2.lin"
filename_cat = "/home/borisov/Dropbox/astro_cologne/work/VinylCyanide/c053515.cat"
compare(filename_test, filename_cat)
