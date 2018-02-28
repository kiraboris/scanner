# python 
#


class StructFactory:
    
    __counter = 0
    
    @staticmethod
    def __next_name():
        StructFactory.__counter = StructFactory.__counter + 1
        name = 'Struct' + str(StructFactory.__counter)
        return name
    
    @staticmethod
    def make(*field_names_only, **field_names_with_def):
        
        all_fields_with_def = field_names_with_def
        all_fields_with_def.update(dict((k, None) for k in field_names_only))
        all_fields = all_fields_with_def.keys()

        # instances of new type get a constructor
        def init_instance(instance, *args, **kwargs):
            
            for k,v in field_names_with_default.items(): # set captured defaults
                setattr(instance, k, v)

            for i in range(len(args)):  # init values for captured field names
                setattr(instance, all_fields[i], args[i])
                
            for k,v in kwargs.items():
                setattr(instance, k, v)
            
            
        return type(StructFactory.__next_name(), (object,), 
            {'__init__': init_instance, '__slots__': all_fields})


class Ranges:
    
    def __init__(self, arrays=[]):
        """'arrays': list of numpy arrays"""

        self.__arrs = arrays
    
    def slices(self, span, step, dim=None)
        """'span': size of slice,
           'step': offset of each next slice from begin of previous one"""
        
        if dim is None:
            xarrs = self.__arrs    
        else:
            xarrs = self.__arrs[:, dim]
        
        bins = [np.arange(a[0]+span/2, a[-1]-span/2, step) for a in xarrs]
        
        def slice_generator():
            for xa, a, b in zib(xarrs, self.__arrs, bins):
                left = 0
                right = 0
                for x in b:
                    while xa[left]  < x - span/2: left  = left  + 1
                    while xa[right] < x + span/2: right = right + 1
                    
                    if dim is None:
                        yield a[left:right]
                    else:
                        yield a[left:right, :]
                    
        return slice_generator
