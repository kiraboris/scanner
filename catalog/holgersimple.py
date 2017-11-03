# python 2.7
import sys
import pickett_io
import quantum_models 


def main(cat_id):
    
    int_fmt    = pickett_io.get_quantum_fmt("c%s.cat"  % cat_id)
    
    lines_cat  = pickett_io.load_cat("c%s.cat"  % cat_id)
#    lines_icat = pickett_io.load_cat("c%si.cat" % cat_id)
    states_egy = pickett_io.load_egy("c%s.egy"  % cat_id, int_fmt)
    
    process(lines_cat)
#    process(lines_icat)
    process(states_egy)
    
    pickett_io.save_cat("c%s_new.cat"  % cat_id, lines_cat)
#    pickett_io.save_cat("c%si_new.cat" % cat_id, lines_icat)
    pickett_io.save_egy("c%s.egy"      % cat_id, states_egy, int_fmt) 


def process(entries):
    old_len = len(entries)
    
    qm = quantum_models.SymmRotorNK()    
#    qm.strip_parity(entries)
    qm.merge_blends(entries)
    
    new_len = len(entries)
    print("Merged %d entries." % (old_len - new_len))  


if __name__ == "__main__":
    if len(sys.argv) < 2: 
        cat_id = raw_input("Enter cat_ID (only digits), please: ")
    else:
        cat_id = sys.argv[1]
        
    main(cat_id)
    
