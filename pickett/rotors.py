
class SymmRotor:
    """symmetric rotor with N, K and possibly v, l, J, hfs""" 
    
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
            
    
