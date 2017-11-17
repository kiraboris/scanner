# python 2.7

import pickett_io
import quantum_models 

cat_id = "041505"

def transform_pseudo_v_into_vl(quanta):
    transormation = {
        0: (0, 0),
        2: (1, -1),
        3: (1, +1),
        6: (2, 0),
        7: (2, +2),
        8: (2, -2)  
    }
    quanta['v'], quanta['l'] = transormation[quanta.get('v', 0)]

def merge_blends(entries):
    old_len = len(entries)
    
    qm = quantum_models.SymmRotor()    
    #qm.strip_parity(entries)
    qm.custom_quanta_transform(entries, transform_pseudo_v_into_vl)
    qm.merge_blends(entries)
    
    new_len = len(entries)
    return old_len - new_len

int_fmt    = pickett_io.get_quantum_fmt("c%s.cat"  % cat_id)

lines_cat  = pickett_io.load_cat("c%s.cat"  % cat_id)
lines_icat = pickett_io.load_cat("c%si.cat" % cat_id)
states_egy = pickett_io.load_egy("c%s.egy"  % cat_id, int_fmt)

num = merge_blends(lines_cat)
print("Cat: reduced %d entries." % num)  

num = merge_blends(lines_icat)
print("ICat: reduced %d entries." % num)  

num = merge_blends(states_egy)
print("Egy: reduced %d entries." % num)  

pickett_io.save_cat("c%s_new.cat"  % cat_id, lines_cat)
pickett_io.save_cat("c%si_new.cat" % cat_id, lines_icat)
pickett_io.save_egy("c%s_new.egy"  % cat_id, states_egy, int_fmt) 
    
