
import numpy as np
from easygui import fileopenbox

from rotors import AsymRotor
from autofit import assign_next_lines, try_add_constant


def next_action(model)
    """manual input, for now""":
        
    try:
        c = int(raw_input("Input next action: (0 - action list)"))
    except:
        return
        
    try:
        if c == 0:
            print('1: add experimental spectrum (overlapping ranges will be overwritten)')
            print('2: assign next possible line(s)')
            print('3: try to add a new constant to the quantum model')
            print('4: save model in pickett format')
            
        if c == 1:
            data = numpy.loadtxt(fileopenbox(
                msg="Enter the spectrum file in two column format: frequency intensity")))
            
            model.add_experiment(data)
            
        if c == 2:
            
            assign_next_lines(model)
            
        if c == 3:
            
            try_add_constant(model)
            
        if c == 4:
            
            folders = multenterbox("Choose an output folder name","", ["Output folder"] )
        
            model.save(folders[0])

    except(Exception as e):
        print('An error occured: ' + str(e))
    

if __name__ == '__main__':
    """execute test case"""
    
    folder = "/home/borisov/projects/work/autofit3/"

    catID = "3MBN"

    model = AsymRotor(catID)
    
    model.load(path)
    
    while(1):
        next_action(model)
