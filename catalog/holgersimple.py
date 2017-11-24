# python 3

import sys
import shutil
from bidict import bidict

import pickett_io
import quantum_models 


def fix_file(in_file, out_file, fmt):
    """docstring"""
    
    print("%s -> %s" % (in_file, out_file))
    entries = pickett_io.load(in_file, fmt)
    old_len = len(entries)

    qm.extract_vl(entries, transormation)
    entries[:] = qm.fix_blends(entries)
    qm.compress_vl(entries, transormation)
    
    new_len = len(entries)
    print("  delta %+d entries." % -(old_len - new_len))  
    pickett_io.save(out_file, entries)
    
    return entries
    

def make_mrg(cat_file, lin_file, egy_file, egy_file_new, mrg_file, fmt):
    """docstring"""
    
    #egy_entries = fix_file(egy_file, egy_file_new, fmt) 
    
    print("Create %s" % (mrg_file))
    
    cat_entries = pickett_io.load(cat_file, fmt)
    lin_entries = pickett_io.load(lin_file, fmt)
    
    mrg_entries = qm.make_mrg(cat_entries, lin_entries)
    
    pickett_io.save(mrg_file, mrg_entries)
    

# *** main part ***

cat_id = "041509"

jobs = ['icat', 'mrg.lin', 'mrg']

qm = quantum_models.SymmRotor()    

transormation = bidict({
    0: (0, 0),
    2: (1, -1),
    3: (1, +1),
    6: (2, 0),
    7: (2, +2),
    8: (2, -2)  
})

if('icat' in jobs):
    int_fmt = pickett_io.get_quantum_fmt("c%si.cat" % cat_id)
elif('cat' in jobs):
    int_fmt = pickett_io.get_quantum_fmt("c%s.cat"  % cat_id)
else:
    sys.exit()
    

if('icat' in jobs): 
    fix_file("c%si.cat" % cat_id, "c%si_new.cat"  % cat_id, int_fmt)

if('cat' in jobs): 
    fix_file("c%s.cat"  % cat_id, "c%s_new.cat"  % cat_id, int_fmt)

if('egy' in jobs): 
    fix_file("c%s.egy"  % cat_id, "c%s_new.egy"  % cat_id, int_fmt)
    
if('mrg.lin' in jobs): 
    fix_file("c%s_mrg.lin"  % cat_id, "c%s_mrg_new.lin"  % cat_id, int_fmt)
    
if('mrg' in jobs):
    make_mrg("c%si_new.cat"  % cat_id, "c%s_mrg_new.lin"  % cat_id,
             "c%s.egy"  % cat_id, "c%s_new.egy" % cat_id, 
             "c%s_new.mrg"  % cat_id, int_fmt)






    
