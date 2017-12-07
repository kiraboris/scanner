# python 3
#
# classes: SymmRotor
#

import math
from numpy import sign
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
        """docstring"""        
        
        # make O(1) lookup dict 
        dict_entries = self.__build_dict(entries)
        
        # merge blends (assuption: entries partitioned into mergable classes)
        result  = []
        ignore  = set()
        for cur in entries:
            
            if cur.qid() in ignore:
                continue
            
            blends  = self._find_mergable(dict_entries, cur)
            
            if(len(blends) > 1):
                result.append(self._merge(blends))
                ignore.update([x.qid() for x in blends])
            else:
                result.append(cur)
                ignore.add(cur.qid())
                
        # make splits        
        result2  = []
        for cur in result:
            
            splits = self._make_splits(dict_entries, cur)
        
            result2.extend(splits)
        
        return result2
    
    
    def __build_dict(self, entries):
        """docstring"""
        
        result = MultiDict()
        for e in entries:
            result.add(e.qid(), e)
            
        return result
        
    
    def make_mrg(self, cat_lst, lin_lst, egy_lst = []):
        """docstring"""
        
        result = []
        
        # process cat entries in lin
        lin_dict = self.__build_dict(lin_lst)
        
        for entry_cat in cat_lst:
            entry_mrg = entry_cat.copy()
            
            if entry_mrg.qid() in lin_dict:
                entry_lin = lin_dict[entry_mrg.qid()]
                
                entry_mrg.freq = entry_lin.freq
                entry_mrg.freq_err = entry_lin.freq_err
                entry_mrg.int_cat_tag = -abs(entry_mrg.int_cat_tag)
                
            result.append(entry_mrg)
        
        # process other lin entries
        ####
        #cat_dict = self.__build_dict(cat_lst)
        #egy_dict = self.__build_dict(egy_lst)
        
        #for entry_lin in lin_lst:
            #if not entry_lin.qid() in cat_dict:
                #entry_mrg = entry_lin.copy()
                #entry_ref = result[0]
                
                #entry_mrg.int_cat_tag = -abs(entry_ref.int_cat_tag)
                #entry_mrg.g 
                
                #result.append(entry_mrg)
        
        return result
            
    
    

class SymmRotor(BasicModel):
    """symmetric rotor with N (aka J), K and possibly v, l""" 
    
    
    def _merge(self, blends):
        """docstring"""
        
        result = blends[0].copy()
        
        if isinstance(result, Line):

            if(self.__spin_symm(result.q_upper) == "A"):
                qu = result.q_upper
                ql = result.q_lower
                ql['K'] = -qu['K']
                result.q_lower = ql
            
            if(not result.log_I is None):
                I_bl = list(map(lambda x: 10 ** x.log_I, blends))
                g_bl = list(map(lambda x: x.g, blends))
                
                result.log_I = math.log10(sum(I_bl))
                
                result.g = 0
                for (I, g) in zip(I_bl, g_bl):
                    if( math.isclose(I, max(I_bl)) ):
                        result.g += g
                #print (list(I_bl), list(g_bl))
                        
                        
            elif(not result.g is None):
                g_bl = map(lambda x: x.g, blends)
                result.g = sum(g_bl)

        elif isinstance(result, State): 
            g_bl = map(lambda x: x.g, blends)
            result.g = sum(g_bl)

        else:
            raise Exception("Neither line nor state")
        
        return result
    
    
    
    def _make_splits(self, dict_entries, entry):
        """docstring"""
        
        if isinstance(entry, Line):
            if(self.__spin_symm(entry.q_upper) == "A"):
                
                result = []
                
                qu = entry.q_upper 
                ql = entry.q_lower
                
                if(sign(qu['K']) == -sign(ql['K'])):
                    result.append(entry)
                
                Kl = abs(ql['K']) 
                Ku = abs(qu['K'])
                
                ql['K'] = Kl
                qu['K'] = -Ku
                if not qid(qu, ql) in dict_entries:
                    newline = entry.copy()
                    newline.q_upper = qu
                    newline.q_lower = ql
                    result.append(newline)

                ql['K'] = -Kl
                qu['K'] = Ku
                if not qid(qu, ql) in dict_entries:
                    newline = entry.copy()
                    newline.q_upper = qu
                    newline.q_lower = ql
                    result.append(newline)        
            else:
                result = [entry]
        else:
            result = [entry]
        
        # debug
        #if math.isclose(entry.freq,  681589.6115 ):
        #    print(len(result))
        #    for x in result:
        #        print(CatConverter.line2str(x))
        
            
        return result

    
    
    def _find_mergable(self, dict_entries, entry):
        """docstring"""
        
        ids = [entry.qid()]
        
        if isinstance(entry, Line):
            if(self.__spin_symm(entry.q_upper) == "A"):
                # build "wrong parity" transition: differs only in q_lower
                
                qu = entry.q_upper 
                ql = entry.q_lower
            
                ql['K'] = -(ql['K'])
                
                ids.append(qid(qu, ql))
            
        result = []
        for x in ids:
            result.extend(dict_entries.getlist(x))
        
        # debug
        #if math.isclose(entry.freq,  681589.6115 ):
        #    print(len(result))
        #    for x in result:
        #        print(CatConverter.line2str(x))
        
        return result
            
            
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
        
        if (abs(quanta['K']) - quanta.get('l', 0)) % 3 == 0:
            return 'A'
        else:
            return 'E'             
            
            
        
    

