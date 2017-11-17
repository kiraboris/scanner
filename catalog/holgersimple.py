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

    qm.custom_quanta_transform(entries, transform_pseudo_v_into_vl)
    entries[:] = qm.merge_blends(entries)
    
    new_len = len(entries)

    print(" reduced %d entries." % (old_len - new_len))  


int_fmt    = pickett_io.get_quantum_fmt("c%s.cat"  % cat_id)

lines_cat  = pickett_io.load_cat("c%s.cat"  % cat_id)
lines_icat = pickett_io.load_cat("c%si.cat" % cat_id)
states_egy = pickett_io.load_egy("c%s.egy"  % cat_id, int_fmt)

print("Cat:")  
merge_blends(lines_cat)

print("ICat:") 
merge_blends(lines_icat)

print("Egy:")  
merge_blends(states_egy)

pickett_io.save_cat("c%s_new.cat"  % cat_id, lines_cat)
pickett_io.save_cat("c%si_new.cat" % cat_id, lines_icat)
pickett_io.save_egy("c%s_new.egy"  % cat_id, states_egy, int_fmt) 
    
