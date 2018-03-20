# python 2,3
#

from bidict import bidict

import catalog
import knowledge

def load_var_into_model(str_filename, obj_rotor):
        fh_var = open("default%s.var"%(str(file_num)))
        for line in fh_var:
            if line.split()[0] == "10000":
                temp_A = float(line.split()[1])
                const_list.append("%.3f" %temp_A)
            if line.split()[0] == "20000":
                temp_B = float(line.split()[1])
                const_list.append("%.3f" %temp_B)
            if line.split()[0] == "30000":
                temp_C = float(line.split()[1])
                const_list.append("%.3f" %temp_C)
    

def get_fit_rms(str_filename):
    
    rms_fit = None
    with open(str_filename) as f:
        for line in reversed(f.readlines()):
            line = line.strip()
            if line[11:14] == "RMS":
                rms_fit = float(line[21:32]) 
                
    return rms_fit
    
    

def _save_parvar_asymm_simple(rotor):
    
    def signum(flag):
        if flag:
            return '+'
        else:
            return '-'
    
    input_file = ""
    input_file += "Molecule                                        Thu Jun 03 17:45:45 2010\n"
    input_file += "   6  430   51    0    0.0000E+000    1.0000E+005    1.0000E+000 1.0000000000\n"
    input_file +="s   1  1  0  99  0  1  1  1  1  -1   0\n"
    input_file += "           10000  %.15e 1.0E%s100 \n" \
        %(rotor.params['A'].value, signum(rotor.params['A'].flag_fit)) 
    input_file += "           20000  %.15e 1.0E%s100 \n" \
        %(rotor.params['B'].value, signum(rotor.params['B'].flag_fit))
    input_file += "           30000  %.15e 1.0E%s100 \n" \
        %(rotor.params['C'].value, signum(rotor.params['C'].flag_fit))
    input_file += "             200  %.15e 1.0E%s100 \n" \
        %(rotor.params['-DJ'].value, signum(rotor.params['-DJ'].flag_fit))
    input_file += "            1100  %.15e 1.0E%s100 \n" \
        %(rotor.params['-DJK'].value, signum(rotor.params['-DJK'].flag_fit)) 
    input_file += "            2000  %.15e 1.0E%s100 \n" \
        %(rotor.params['-DK'].value, signum(rotor.params['-DK'].flag_fit))
    
    fh_var = open("output.var",'w')
    fh_var.write(input_file)
    fh_var.close()




class RotorParameter(object):
    
    def __init__(self, code, value=1.0, error=float('inf')):
        self.code = code
        self.value = value
        self.error = error
        self.flag_fit = False

def save_int(str_filename, obj_rotor, 
            J_min=0, J_max=100, inten=-15.0, max_freq=300.0, temperature=300.0):
    
    input_file = ""
    input_file += "%s \n" % obj_rotor.name
    input_file += ("0  91  %f  %3d  %3d  %f  %f  %f  %f\n" % 
        (obj_rotor.Q(temperature), J_min, J_max, inten, inten,
         max_freq, temperature))
         
    if obj_rotor.u_A:
        input_file += " 001  %f \n" % obj_rotor.u_A
        
    if obj_rotor.u_B:
        input_file += " 002  %f \n" % obj_rotor.u_B
        
    if obj_rotor.u_C:
        input_file += " 003  %f \n" % obj_rotor.u_C

    with open(str_filename, "w") as fh:
        fh.write(input_file)


def save_par(str_filename, obj_rotor):
    
    if all([x in self.params for x in ['A', 'B', 'C', '-DJ', '-DJK', '-DK']]):
        _save_parvar_asymm_simple(obj_rotor)
    else:
        raise NotImplementedError
        


class RotorSymmetry:
    
    def __init__(self):
        # sample defaults
        self.rotor_type = "asym"
        self.symmetry_type = 'C3v'
        self.representation = 'IIIr'
        self.reduction = 'S'
        self.degree = 3

class Rotor(object):
    
    def __init__(self):
        
        self.enabled_params = {}
        self.disabled_params = {}
        
        self.symmetry = RotorSymmetry()
        
        
    def param(name_or_code):
        
        if isinstance(name_or_code, str):
            code = knowledge.param_code(name_or_code)
        else:
            code = name_or_code
            
        par = enabled_params.get(code, None)
        
        if par is None:
            par = disabled_params.get(code, None)
            
        return par
                     
    
    def Q(self, T): 
        
        if self.symmetry.rotor_type == "asym":
            QrotBase = (self.param('A').value *
                        self.param('B').value *
                        self.param('C').value)**(-0.5)
        elif self.symmetry.rotor_type == "sym":
            QrotBase = (self.param('A').value *
                        self.param('B').value**2)**(-0.5) 

            Qrot = ((5.3311 * 10**(6)) * (T**(1.5)) * QrotBase
            
        return Qrot
        
        
