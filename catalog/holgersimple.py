# python 2.7
import sys
import pickett_io
import quantum_models 

def main(filename):
    
    qm = quantum_models.SymmRotorNK()
    
    int_fmt    = pickett_io.get_quantum_fmt(filename + ".cat")
    
    lines_cat  = pickett_io.load_cat(filename + ".cat")
    #lines_icat = pickett_io.load_cat(filename + "i.cat")
    states_egy = pickett_io.load_egy(filename + ".egy", int_fmt)
    print len(lines_cat)
    qm.merge_blends(lines_cat)
    print len(lines_cat)

    #qm.merge_blends(lines_icat)
    qm.merge_blends(states_egy)
    
    pickett_io.save_cat(filename + "_new.cat", lines_cat)
    #pickett_io.save_cat(filename + "i_new.cat", lines_icat)
    pickett_io.save_egy(filename + "_new.egy", states_egy, int_fmt)


def test(filename):
    int_fmt    = pickett_io.get_quantum_fmt(filename + ".cat")
    print(int_fmt)
    lines_cat  = pickett_io.load_cat(filename + ".cat")
    states_egy = pickett_io.load_egy(filename + ".egy",int_fmt)    
    pickett_io.save_cat(filename + "_new.cat", lines_cat)
    pickett_io.save_egy(filename + "_new.egy", states_egy, int_fmt)    
    
if __name__ == "__main__":
    main("test2")