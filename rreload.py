# http://stackoverflow.com/questions/15506971/recursive-version-of-reload
#     """Recursively reload modules."""

from types import ModuleType;

recursionDepth = 2;
def rel(module):
    _do(module, recursionDepth);

def _do(module, depth):
    if(depth <= 0):
        return;

    try:
        reload(module);
    except:
        pass;
    
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name);
        if type(attribute) is ModuleType:
            _do(attribute, depth - 1);