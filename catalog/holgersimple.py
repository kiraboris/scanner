# python 2.7
import sys
import pickett_io
import quantum_models 

def main(filename):
    
    qm = quantum_models.SymmRotorNK()
    
    int_fmt    = pickett_io.get_quantum_fmt(filename + ".cat")
    
    lines_cat  = pickett_io.load_cat(filename + ".cat")
    lines_icat = pickett_io.load_cat(filename + ".icat")
    states_egy = pickett_io.load_egy(filename + ".egy", int_fmt)
    
    qm.merge_blends(lines_cat)
    qm.merge_blends(lines_icat)
    qm.merge_blends(states_egy)
    
    pickett_io.save_cat(filename + "_new.cat", lines_cat)
    pickett_io.save_cat(filename + "_new.icat", lines_icat)
    pickett_io.save_egy(filename + "_new.egy", states_egy, int_fmt)


def test():
    int_fmt    = pickett_io.get_quantum_fmt("test.cat")
    lines_cat  = pickett_io.load_cat("test.cat")
    states_egy = pickett_io.load_egy("test.egy")    
    pickett_io.save_cat("test_new.icat", lines_icat)
    pickett_io.save_egy("test_new.egy",  states_egy, int_fmt)    
    
if __name__ == "main":
    test()