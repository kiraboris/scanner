# python 3

import sys
import shutil
from bidict import bidict

import pickett_io
from pickett_corrector import Corrector, SymmRotor

flag13Cvib = True

if not flag13Cvib:
    transormation = bidict({
        0: ((0, 0, 0),  0, 0),
        2: ((1, 0, 0), -1, 0),
        3: ((1, 0, 0), +1, 0),
        6: ((2, 0, 0),  0, 0),
        7: ((2, 0, 0), +2, 0),
        8: ((2, 0, 0), -2, 0), 
        12:((0, 0, 1),  0, 0),
        14:((0, 1, 0), -1, 0),
        15:((0, 1, 0), +1, 0),
        18:((0, 0, 3), -1, 0),
        19:((0, 0, 3), +1, 0),
        20:((0, 0, 1), -3, 0),
        21:((0, 0, 1), +3, 0),
        1: ((0, 0, 0),  0, 1),
        4: ((1, 0, 0), -1, 1),
        5: ((1, 0, 0), +1, 1),
        9: ((2, 0, 0),  0, 1),
        10:((2, 0, 0), +2, 1),
        11:((2, 0, 0), -2, 1)    
    })
else:
    transormation = bidict({
        0: ((1, 0, 0),  -1, 0),
        1: ((1, 0, 0),  +1, 0),
    })
    
    

def _extract_v(quanta):
    """docstring"""
    
    quanta['v'], quanta['l'], quanta['hfs'] = transormation[quanta.get('v', 0)]
    return quanta


def _compress_v(quanta):
    """docstring"""

    quanta['v'] = transormation.inv[(quanta['v'], quanta['l'], quanta['hfs'])]
    return quanta


qm = Corrector(SymmRotor())   

looper = {"042515": ['icat', 'lin', 'mrg', 'egy']}

#looper = {"042508": ['egy'], "042509": ['egy']} 

#looper = {"042513": ['egy'], "042514": ['egy']}

#int_fmt_override = 1303 

def fix_file(in_file, out_file, fmt):
    """docstring"""
    
    print("%s -> %s" % (in_file, out_file))
    entries = pickett_io.load(in_file, fmt)
    old_len = len(entries)

    qm.custom_quanta_transform(entries, _extract_v)
    entries[:] = qm.correct(entries, in_file[-3:])
    qm.custom_quanta_transform(entries, _compress_v)
    
    new_len = len(entries)
    print("  delta %+d entries." % -(old_len - new_len))  
    pickett_io.save(out_file, entries)
    
    return entries
    

def make_mrg(cat_file, lin_file, egy_file, egy_file_new, mrg_file, fmt):
    """docstring"""
    
    print("Create %s" % (mrg_file))
    
    cat_entries = pickett_io.load(cat_file, fmt)
    lin_entries = pickett_io.load(lin_file, fmt)
    
    mrg_entries = qm.make_mrg(cat_entries, lin_entries)
    
    pickett_io.save(mrg_file, mrg_entries)
    

# *** main part ***
for cat_id in looper:
    
    jobs = looper[cat_id]
    
    if "int_fmt_override" in globals():
        int_fmt = int_fmt_override
    elif('icat' in jobs):
        int_fmt = pickett_io.get_quantum_fmt("c%si.cat" % cat_id)
    elif('cat' in jobs):
        int_fmt = pickett_io.get_quantum_fmt("c%s.cat"  % cat_id)
    else:
        print('Nowhere to get format from..(')
        sys.exit()
        

    if('icat' in jobs): 
        fix_file("c%si.cat" % cat_id, "c%si_new.cat"  % cat_id, int_fmt)
        icat_fname = "c%si_new.cat"

    if('cat' in jobs): 
        fix_file("c%s.cat"  % cat_id, "c%s_new.cat"  % cat_id, int_fmt)
        icat_fname = "c%s_new.cat"

    if('egy' in jobs): 
        fix_file("c%s.egy"  % cat_id, "c%s_new.egy"  % cat_id, int_fmt)
        
    if('lin' in jobs): 
        fix_file("c%s.lin"  % cat_id, "c%s_new.lin"  % cat_id, int_fmt)
        lin_fname = "c%s_new.lin"
    
    if('mrg.lin' in jobs): 
        fix_file("c%s_mrg.lin"  % cat_id, "c%s_mrg_new.lin"  % cat_id, int_fmt)
        lin_fname = "c%s_mrg_new.lin"
        
    if('mrg' in jobs):
        make_mrg(icat_fname % cat_id, lin_fname % cat_id,
                 "c%s.egy"  % cat_id, "c%s_new.egy" % cat_id, 
                 "c%s_new.mrg"  % cat_id, int_fmt)



