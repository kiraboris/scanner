# python 3
#
# classes: SymmRotor
#

import math
from functools import partial as bind
from werkzeug.datastructures import MultiDict

from basic_structs import Line, State, qid

class BasicModel:
    """general methods on transitions and states"""
    
    
    def custom_quanta_transform(self, entries, func_transform):
        """docstring"""

        for entry in entries:
            if hasattr(entry, "q"):
                entry.q = func_transform(entry.q)
                
            elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
                entry.q_upper = func_transform(entry.q_upper)
                entry.q_lower = func_transform(entry.q_lower)
    
    
    
    def fix_blends(self, entries):
        
        # make O(1) lookup dict 
        dict_entries = self.__build_dict(entries)
        
        # merge blends (assuption: entries partitioned into mergable classes)
        result  = []
        ignore  = set()
        for i in range(0, len(entries)):
            
            if entries[i].qid() in ignore:
                continue
            
            blends  = self._find_mergable(dict_entries, entries[i])
            
            if(len(blends) > 1):
                result.append(self._merge(blends))
                ignore.update([x.qid() for x in blends])
            else:
                result.append(entries[i])
                ignore.add(entries[i].qid())
                
        # make splits        
        entries = result
        result  = []
        for i in range(0, len(entries)):
            
            splits = self._make_splits(dict_entries, entries[i])
        
            result.extend(splits)
        
        return result
    
    
    def __build_dict(self, entries):
        """docstring"""
        
        result = MultiDict()
        for e in entries:
            result.add(e.qid(), e)
            
        return result
        
    
    
    

class SymmRotor(BasicModel):
    """symmetric rotor with N (aka J), K and possibly v, l""" 
    
    def __pv2vl(self, quanta, mapper):
        """docstring"""
        
        quanta['v'], quanta['l'] = mapper[quanta.get('v', 0)]
        return quanta
    
    
    def __vl2pv(self, quanta, mapper):
        """docstring"""

        quanta['v'] = mapper.inv[(quanta['v'], quanta['l'])]
        return quanta
    
    
    def extract_vl(self, entries, mapper):
        """docstring"""
        
        self.custom_quanta_transform(entries, bind(self.__pv2vl, mapper=mapper))
        
        
    def compress_vl(self, entries, mapper):
        """docstring"""
       
        self.custom_quanta_transform(entries, bind(self.__vl2pv, mapper=mapper))
    
    
    def __spin_symm(self, quanta):
        """get spin-statistical symmetry irr.rep. of state or line"""
        
        if (quanta['K'] - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'
    
    
    def _merge(self, blends):
        """docstring"""
        
        result = blends[0].copy()
        
        if isinstance(result, Line):

            if(self.__spin_symm(result.q_upper) == "A"):
                result.q_lower['K'] = -(result.q_upper['K'])
            
            if(not result.log_I is None):
                I_bl = map(lambda x: 10 ** x.log_I, blends)
                g_bl = map(lambda x: x.g, blends)
                
                result.log_I = math.log10(sum(I_bl))
                
                result.g = 0
                for (I, g) in zip(I_bl, g_bl):
                    if( I == max(I_bl) ):
                        result.g += g
                        
            elif(not result.g is None):
                g_bl = map(lambda x: x.g, blends)
                result.g = sum(g_bl)

        elif isinstance(result, State): 
            g_bl = map(lambda x: x.g, blends)
            result.g = sum(g_bl)

        else:
            raise Exception("Neigher line nor state")
        
        return result
    
    
    
    def _make_splits(self, dict_entries, entry):
        """docstring"""
        
        if isinstance(entry, Line):
            if(self.__spin_symm(entry.q_upper) == "A"):
                
                result = []
                
                qu = entry.q_upper 
                ql = entry.q_lower
                
                if(ql['K'] == -(qu['K'])):
                    result.append(entry)
                
                K = abs(ql['K']) # == abs(qu[K])
                
                ql['K'] = K
                qu['K'] = -K
                if not qid(qu, ql) in dict_entries:
                    newline = entry.copy()
                    newline.q_upper = qu
                    newline.q_lower = ql
                    result.append(newline)
                
                ql['K'] = -K
                qu['K'] = K
                if not qid(qu, ql) in dict_entries:
                    newline = entry.copy()
                    newline.q_upper = qu
                    newline.q_lower = ql
                    result.append(newline)        
            else:
                result = [entry]
        else:
            result = [entry]
                
        #if(entry.freq == 73805.7356):
        #    print( [x.qid() for x in result] )
            
        return result

    
    
    def _find_mergable(self, dict_entries, entry):
        """docstring"""
        
        ids = [entry.qid()]
        if isinstance(entry, Line):
            if(self.__spin_symm(entry.q_upper) == "A"):
                # build "wrong parity" transition quanta
                
                qu = entry.q_upper 
                ql = entry.q_lower
            
                ql['K'] = -(ql['K'])
                
                ids.append(qid(qu, ql))
            
        result = []
        for x in ids:
            result.extend(dict_entries.getlist(x))
        
        #if(entry.freq == 73805.7356):
        #    print( [x.qid() for x in result] )
        
        return result
            
            
             
            
            
        
    

