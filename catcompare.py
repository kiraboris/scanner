
from pickett_old import pickett

def signum(line):
    if line.int_cat_tag > 0:
        return " "
    else:
        return "+"

def print_line(line, real_line):
    print("Frequency: {:.4f}, actual frequency {}{:.4f}".
          format(line.freq, signum(real_line), real_line.freq), end='')

def criterium(line, real_line, crit):
    return abs(line.freq - real_line.freq) < crit


def compare(filename_test, filename_cat):

    crit = .10   #MHz

    print('Comparing linelists with {:.3f} MHz allowance'.format(crit))
    fmt = pickett.get_quantum_fmt(filename_cat)
    new_fmt = fmt - fmt % 10 + 3
    linelist_test = pickett.load_pgo_lin(filename_test, new_fmt)
    linelist_cat = pickett.load_cat(filename_cat)
    linelist_cat_dict = pickett.make_dict(linelist_cat, new_fmt)

    u, v = 0,0
    for line in linelist_test:
        if line.qid() in linelist_cat_dict:
            line_real = linelist_cat_dict[line.qid()]
            print_line(line, line_real)
            if not criterium(line, line_real, crit):
                print(" --> mismatch!")
                u += 1
            else:
                print(" --> ok")
                v += 1

    print(v / (u+v))
        

filename_test = "C:/Users/Kirill/Dropbox/astro_cologne/work/mbn/current.lin"
filename_cat = "C:/Users/Kirill/Dropbox/astro_cologne/work/mbn/current.cat"
compare(filename_test, filename_cat)
