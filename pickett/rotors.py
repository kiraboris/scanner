# python 2,3
#

import math
import numpy as np

import catalog

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
        %(-rotor.params['-DJ'].value, signum(rotor.params['-DJ'].flag_fit))
    input_file += "            1100  %.15e 1.0E%s100 \n" \
        %(-rotor.params['-DJK'].value, signum(rotor.params['-DJK'].flag_fit)) 
    input_file += "            2000  %.15e 1.0E%s100 \n" \
        %(-rotor.params['-DK'].value, signum(rotor.params['-DK'].flag_fit))
    
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
            J_min=0, J_max=20, inten1=-10.0, max_freq=100.0, temperature=300.0):
    
    input_file = ""
    input_file += "%s \n" % obj_rotor.name
    input_file += ("0  91  %f  %3d  %3d  %f  %f  %f  %f\n" % 
        (obj_rotor.Q(temperature), J_min, J_max, inten, inten,
         max_freq, temperature))
    input_file += " 001  %f \n" % obj_rotor.u_A
    input_file += " 002  %f \n" % obj_rotor.u_B
    input_file += " 003  %f \n" % obj_rotor.u_C

    with open(str_filename, "w") as fh:
        fh.write(input_file)


def save_par_var(str_filename, obj_rotor):
    
    if all([x in self.params for x in ['A', 'B', 'C', '-DJ', '-DJK', '-DK']]):
        _save_parvar_asymm_simple(obj_rotor)
    else:
        raise NotImplementedError
        


class Rotor(object):
    """symmetric rotor with N, K and possibly v, l, J, hfs""" 
    
    def __init__(self):
        
        self.__symmetry = Symmetry()
        self.__formatter = formatter.Formatter(SymmCorrector(self.__symmetry))

        self.params = {}
    
    def Q(self, T): 
        if all([x in self.params for x in ['A', 'B', 'C']]):
            Qrot = ((5.3311 * 10**(6)) * (float(T)**(1.5)) * 
                    (float(self.params['A']) *
                     float(self.params['B']) *
                     float(self.params['C']))**(-0.5))
        else:
            Qrot = BasicRotor.Q(self, T)
            
        return Qrot
        
        
class SymmCorrector:
    
    def __init__(self, symmetry):
        
        self.__symm = symmetry

    def merge_lines(self, blends):
        """docstring"""
        
        result = blends[0].copy()
        
        if not result.g is None:
            if not result.log_I is None:
                I_bl = list(map(lambda x: 10 ** x.log_I, blends))
                g_bl = list(map(lambda x: x.g, blends))
                
                result.log_I = math.log10(sum(I_bl))
                
                result.g = 0
                for (I, g) in zip(I_bl, g_bl):
                    if( math.isclose(I, max(I_bl)) ):
                        result.g += g
            else:
                g_bl = map(lambda x: x.g, blends)
                result.g = sum(g_bl)
        
        return result
    
    
    def merge_states(self, blends):
        """docstring"""
        
        result = blends[0].copy()
        
        g_bl = map(lambda x: x.g, blends)
        result.g = sum(g_bl)

        return result    
    
    
    def __split_blended_line(self, entry):
        
        result = []
        
        qu = entry.q_upper 
        ql = entry.q_lower
        Kl = abs(ql['K']) 
        Ku = abs(qu['K'])
        
        ql['K'] = Kl
        qu['K'] = -Ku
        newline = entry.copy()
        newline.q_upper = qu
        newline.q_lower = ql
        if not newline.g is None:
            newline.g = newline.g / 2
        result.append(newline)

        ql['K'] = -Kl
        qu['K'] = Ku
        newline = entry.copy()
        newline.q_upper = qu
        newline.q_lower = ql
        if not newline.g is None:
            newline.g = newline.g / 2
        result.append(newline)
        
        return result
    
    
    def split_line(self, dict_entries, entry, flag_strict):
        """docstring"""
        
        if(self.__spin_symm(entry) == "A"):
            
            result = []
            
            qu = entry.q_upper 
            ql = entry.q_lower
            
            if(ql['K'] == 0 or qu['K'] == 0):
                result.append(entry)
            else:
                if(np.sign(qu['K']) == -np.sign(ql['K'])): # Ku == -Kl mod 2, correct
                    if(not flag_strict):
                        result.append(entry)
                    else:
                        # always require l-splitting
                        ql['K'] = -ql['K']
                        qu['K'] = -qu['K']
                        if qid(qu, ql) in dict_entries:
                            # other parity is there
                            result.append(entry)
                        else:
                            # other parity is NOT there: entry is a blended line
                            result.extend(self.__split_blended_line(entry))
                else:
                    # Ku == +Kl mod 2, incorrect
                    Kl = abs(ql['K']) 
                    Ku = abs(qu['K'])
                    
                    qu['K'] = Ku
                    ql['K'] = -Kl
                    qid_plus_to_minus = qid(qu, ql)
                    
                    qu['K'] = -Ku
                    ql['K'] =  Kl
                    qid_minus_to_plus = qid(qu, ql)
                    
                    if( qid_plus_to_minus in dict_entries and 
                        not qid_minus_to_plus in dict_entries):
                        # make "minus_to_plus" from entry
                        qu['K'] = -Ku
                        ql['K'] =  Kl 
                        entry.q_upper = qu
                        entry.q_lower = ql  
                        result.append(entry)
                    elif( qid_minus_to_plus in dict_entries and 
                          not qid_plus_to_minus in dict_entries): 
                        # make "plus_to_minus" from entry
                        qu['K'] = -Ku
                        ql['K'] =  Kl
                        entry.q_upper = qu
                        entry.q_lower = ql  
                        result.append(entry)
                    elif( qid_minus_to_plus in dict_entries and 
                          qid_plus_to_minus in dict_entries): 
                        # entry is redundant
                        pass
                    else:
                        # entry is a blended line, create both splits
                        result.extend(self.__split_blended_line(entry))
                           
        else:
            # E-symmetry line doesn't need splitting
            result = [entry]
            
        return result
    
    
    def split_state(self, dict_entries, entry):
        """docstring"""
        
        # state doesn't need splitting
        result = [entry]        
            
        return result

    
    
    def find_mergable_with_line(self, dict_entries, entry):
        """docstring"""
        
        ids = [entry.qid()]
        
        if(self.__spin_symm(entry) == "A"):
            # merge with 'wrong parity' transition
            # that differs only in q_lower
            
            qu = entry.q_upper 
            ql = entry.q_lower
        
            ql['K'] = -(ql['K'])
            
            ids.append(qid(qu, ql))
            
        result = []
        for x in ids:
            result.extend(dict_entries.getlist(x))
        
        return result
        
    
    def find_mergable_with_state(self, dict_entries, entry):
        """docstring"""
        
        # only states with same qid() are mergable
        result = dict_entries.getlist(entry.qid())
        
        return result
        
    def __spin_symm_q(self, quanta):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if quanta['K'] == 0 and quanta.get('l', 0) % 3 == 0:
            return 'E'        
        elif (abs(quanta['K']) - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'             
    
    
    def __spin_symm(self, entry):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if isinstance(entry, Line):             
            upper = self.__spin_symm_q(entry.q_upper)
            lower = self.__spin_symm_q(entry.q_lower)
            if upper == "A" or lower == "A":
                return 'A'
            else:
                return 'E'
        elif isinstance(entry, State):
            return self.__spin_symm_q(entry.q)
        else:
            raise Exception('Neither line nor state')


class Symmetry:

    def spin_symm_q(self, quanta):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if quanta['K'] == 0 and quanta.get('l', 0) % 3 == 0:
            return 'E'        
        elif (abs(quanta['K']) - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'             
    
    
    def spin_symm(self, entry):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if isinstance(entry, Line):             
            upper = self.__spin_symm_q(entry.q_upper)
            lower = self.__spin_symm_q(entry.q_lower)
            if upper == "A" or lower == "A":
                return 'A'
            else:
                return 'E'
        elif isinstance(entry, State):
            return self.__spin_symm_q(entry.q)
        else:
            raise Exception('Neither line nor state')
            
