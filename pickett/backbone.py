
from . import knowledge
from .autofit import load_model

def improve(model):
    """manual input, for now"""
        
    try:
        c = int(knowledge.ask("Input next action: (0 - action list)"))
    except:
        return
        
    try:
        if c == 0:
            print('1: add experimental spectrum (overlapping ranges will be overwritten)')
            print('2: assign next possible line(s)')
            print('3: try to add a new constant to the quantum model')
            print('4: save model in pickett format')
            
        if c == 1:
            file = (knowledge.ask_filename(
                msg="Enter the spectrum file in two column format: frequency intensity"))
            
            model.add_experiment(file)
            
        if c == 2:
            
            model = fitter.assign_next_lines(model)
            
        if c == 3:
            model = fitter.try_add_constant(model)
            
        if c == 4:
            
            model.save()

    except Exception as e:
        print('An error occured: ' + str(e))
    

if __name__ == '__main__':
    """execute test case"""
    
    folder = "/home/borisov/projects/work/autofit3/"

    catID = "3MBN"

    model = load_model(catID, folder)
    
    model = improve(model)
