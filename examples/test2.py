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
    return [open(url).read()]


# Render the template
output = template({'a':123}, helpers={'include', _include})

print(output)