# python 3

import sys
import shutil
import bidict

import rotors

def main():

    transormation1 = bidict.bidict({
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
    
    transormation2 = bidict.bidict({
        0: ((1, 0, 0),  -1, 1),
        1: ((1, 0, 0),  +1, 1),
    })
    
    transormation3 = bidict.bidict({
        5: ((1, 0, 0),  -1, 1),
        6: ((1, 0, 0),  +1, 1),
    })
    
    
    qm = Corrector(SymmRotor())   

    looper = {"042514_hfs": ['cat', 'lin', 'mrg', 'egy']}

    #int_fmt_override = 1303 

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


def extract_v(quanta):
    """docstring"""
    
    v = quanta.get('v', 0)
    
    if v == 0:
        v = 5
    if v == 1:
        v = 6
    
    quanta['v'], quanta['l'], quanta['hfs'] = transormation[v]
    return quanta


def compress_v(quanta):
    """docstring"""
    quanta['v'] = transormation.inv[(quanta['v'], quanta['l'], quanta['hfs'])]
    return quanta


def load(str_filename, int_quanta_fmt):
    """docstring"""
    
    extension = str_filename[-3:]
    
    if( extension == "cat" or extension == "mrg" ):
        return load_cat(str_filename)
        
    if( extension == "egy" ):
        return load_egy(str_filename, int_quanta_fmt)
        
    if( extension == "lin" ):
        return load_lin(str_filename, int_quanta_fmt)



def save(str_filename, lst_entries):
    """docstring"""
    
    extension = str_filename[-3:]
    
    if( extension == "cat" or extension == "mrg" ):
        save_cat(str_filename, lst_entries)
        
    if( extension == "egy" ):
        save_egy(str_filename, lst_entries)
        
    if( extension == "lin" ):
        save_lin(str_filename, lst_entries)
        

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
    
if __name__ == "__main__":
    main()
