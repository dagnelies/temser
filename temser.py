import pystache
import re
import os.path
import json
import urllib.request
import bottle

'''
Flow of execution:

1. fetch all include
2. replace $args with their argument values
3. fetch data sources
4. apply templating

'''

def remote_fetch(path):
    content = urllib.request.urlopen("http://example.com/foo/bar").read()
    return content
    
    
def local_fetch(path, root):
    fullpath = os.path.abspath( os.path.join(root, path.strip('/\\')) )
    
    if not fullpath.startswith(root):
        raise Exception("Access denied: %s" % path)
    
    with open(fullpath) as f:
        content = f.read()
        
    return content
    

_params_re = re.compile('\$\w+')
_code_re = re.compile('<\?.+\?>')


class TemSer:
    
    def __init__(self, root='.', local=True, hooks={}):
        self.root = os.path.abspath(root) + os.sep
        self.local = local
        self.hooks = hooks
        
    def fetch(self, path, parsed):
        if self.hooks:
            for k,v in self.hooks.items():
                if path.startswith(k):
                    return v(path, format)
        
        if path.startswith('http://') or path.startswith('https://'):
            if self.local:
                raise Exception('Remote content not allowed in local mode.')
            else:
                content = remote_fetch(path)
        else:
            try:
                content = local_fetch(path, self.root)
            except Exception as e:
                raise Exception('Invalid path: %s' % path, e)
                
        if not parsed:
            return content
        else:
            return json.loads(content)
            
            
    def render(self, path, **kwargs):
        template = self.fetch(path, False)
        
        # fetch all includes (possibly caching the result)
        template = self.resolve_includes(template)
        
        # replace $args with their argument values
        template = self.replace_params(template, **kwargs)
        
        # fetch data sources
        template, data = self.gather_data(template)
        
        # apply templating
        template = pystache.render(template, data)
        
        # check for remaining tags
        m = _code_re.search(template)
        if m:
            raise Exception('Invalid tag: %s' % m.group(0))
            
        return template

    def resolve_includes(self, template):
        #print(template)
        def replace_include(match):
            tag = match.group(0)
            tokens = tag[2:-2].strip().split()
            if tokens[0] != 'include':
                # leave it unchanged
                return tag
            
            if len(tokens) != 2:
                raise Exception('A single token is expected after include instead of: %s' % tag)
                
            path = tokens[1]
            template = self.fetch(path, False)
            return self.resolve_includes(template)
            
        template = _code_re.sub(replace_include, template)    
        return template


    def replace_params(self, template, **kwargs):
        def replace_param(m):
            k = m.group(0)[1:]
            if k in kwargs:
                return kwargs[k]
            else:
                return ''
        
        template = _params_re.sub(replace_param, template)
        return template
    
    
    def gather_data(self, template):
        data = {}
        def extract_data(match):
            tag = match.group(0)
            tokens = tag[2:-2].strip().split()
            
            if len(tokens) != 3 or tokens[1] != '=':
                return tag
                
            key = tokens[0]
            value = tokens[2]
            if key in data and data[key] != value:
                raise Exception('Data item "%s" is defined twice with different values!' % key)
            data[key] = value
            return ''
            
        template = _code_re.sub(extract_data, template)    
        
        for k,v in data.items():
            value = self.fetch(v, True)
            data[k] = value
        
        return template, data
        

    def run(self, **kwargs):
        app  = bottle.Bottle()
        
        @app.get('')    
        @app.get('/')
        def index():
            for file in ['index.tml', 'index.html']:
                if os.path.exists( os.path.join(self.root, file) ):
                    return serve(file)
                    
            bottle.abort(404)
        
        @app.get('<path:path>')
        def serve(path):
            if path.endswith('.tml'):
                params = bottle.request.params
                return self.render(path, **params)
            else:
                return bottle.static_file(path, root=self.root)
            
        app.run(**kwargs)
