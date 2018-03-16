# python 2,3
#

import math
import numpy as np
from werkzeug.datastructures import MultiDict

from types import Line, State, qid

class Corrector:
    """general methods on transitions and states"""
    
    def __init__(self, model):
        self.__model = model
    
    
    def custom_quanta_transform(self, entries, func_transform):
        """docstring"""

        for entry in entries:
            if hasattr(entry, "q"):
                entry.q = func_transform(entry.q)
                
            elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
                entry.q_upper = func_transform(entry.q_upper)
                entry.q_lower = func_transform(entry.q_lower)
    
    
    def correct(self, entries, file_format):
        """docstring"""        
        
        # make O(1) lookup dict 
        dict_entries = self.__build_dict(entries)
        
        # merge blends (assumption: entries partitioned into mergable classes)
        result  = []
        ignore  = set()
        for cur in entries:
            
            if cur.qid() in ignore:
                continue
            
            blends = self.__find_mergable(dict_entries, cur, file_format)
            
            if(len(blends) > 1):
                result.append(self.__merge(blends, file_format))
                ignore.update([x.qid() for x in blends])
            else:
                result.append(cur)
                ignore.add(cur.qid())
                
        # make splits        
        result2  = []
        for cur in result:
            
            splits = self.__split(dict_entries, cur, file_format)
        
            result2.extend(splits)
            
            dict_entries.update(self.__build_dict(splits))
        
        return result2
    
    
    def make_mrg(self, cat_lst, lin_lst, egy_lst = []):
        """look for cat entries in lin and merge the two files into mrg"""
        
        result = []
        
        lin_dict = self.__build_dict(lin_lst)
        
        for entry_cat in cat_lst:
            entry_mrg = entry_cat.copy()
            
            if entry_mrg.qid() in lin_dict:
                entry_lin = lin_dict[entry_mrg.qid()]
                
                entry_mrg.freq = entry_lin.freq
                entry_mrg.freq_err = entry_lin.freq_err
                entry_mrg.int_cat_tag = -abs(entry_mrg.int_cat_tag)
                
            result.append(entry_mrg)
        
        return result
    
    
    def __find_mergable(self, dict_entries, cur, file_format):
        
        if 'cat' in file_format or 'lin' in file_format:
            return self.__model.find_mergable_with_line(dict_entries, cur)
        elif 'egy' in file_format:
            return self.__model.find_mergable_with_state(dict_entries, cur)
        else:
            raise Exception('File format unknown') 
    
    
    def __merge(self, blends, file_format):
        
        if 'cat' in file_format or 'lin' in file_format:
            return self.__model.merge_lines(blends)
        elif 'egy' in file_format:
            return self.__model.merge_states(blends)
        else:
            raise Exception('File format unknown') 
    

    def __split(self, dict_entries, cur, file_format):
        
        if 'cat' in file_format:
            return self.__model.split_line(dict_entries, cur, flag_strict=True)
        elif 'lin' in file_format:
            return self.__model.split_line(dict_entries, cur, flag_strict=False)
        elif 'egy' in file_format:
            return self.__model.split_state(dict_entries, cur)
        else:
            raise Exception('File format unknown') 
        
    
    def __build_dict(self, entries):
        """docstring"""
        
        result = MultiDict()
        for e in entries:
            result.add(e.qid(), e)
            
        return result
    
    



