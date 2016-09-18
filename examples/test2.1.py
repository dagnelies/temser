import json

source = open('test.tmd').read()

# Get a compiler
from pybars import Compiler
compiler = Compiler()

# Compile the template
template = compiler.compile(source)

# Add any special helpers
def _fetch(data, options, *kargs, **kwargs):
    var = kargs[0]
    url = options['fn'](data).pop()
    print(url)
    raw = open(url).read()
    data[var] = json.loads(raw)
    return ''

def _include(data, options, *kargs, **kwargs):
    url = options['fn'](data).pop()
    print(url)
    return open(url).read()

class p(dict):
    def __init__(self):
        pass
    
    def __get__(self, key):
        return 'incl - ' + key
        
    
# Render the template
output = template({'a':123}, partials=p())

print(output)