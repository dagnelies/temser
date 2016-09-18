import pybars
import re
import os.path
import json
import urllib.request
import bottle
import markdown

'''
Flow of execution:

1. fetch all include
2. replace $args with their argument values
3. fetch data sources
4. apply handlebars or markdown first templating

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
_include_re = re.compile('\{\{>>(.+)\}\}')

class TemSer:
    
    def __init__(self, root='.', local=True, hooks={}, theme=None):
        self.root = os.path.abspath(root) + os.sep
        self.local = local
        self.hooks = hooks
        self.server = None
        self.theme = theme
        
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
            
    
    def render2(self, template, data):
        pass
    
    def render(self, path, **kwargs):
        template = self.fetch(path, False)
        
        # fetch all includes (possibly caching the result)
        template = self.resolve_includes(template)
        
        # replace $args with their argument values
        template = self.replace_params(template, **kwargs)
        
        # fetch data sources
        template, data = self.gather_data(template)

        # check for remaining tags
        m = _code_re.search(template)
        if m:
            raise Exception('Invalid tag: %s' % m.group(0))
        
        # apply handlebars templating
        c = pybars.Compiler()
        hbs = c.compile(template)
        template = hbs(data)

        # apply markdown
        template = markdown.markdown(template)

        # insert into theme
        if self.theme:
            path = self.theme['path'] + '/theme.html'
            empty = self.fetch(path, False)
            #print(empty)
            hbs = c.compile(empty)
            empty = hbs({'@theme': self.theme})
            template = empty.replace('<?content?>', template)
            
        return template

    def resolve_includes(self, template):
        #print(template)
        def replace_include(match):
            path = match.group(1)
            template = self.fetch(path, False)
            return self.resolve_includes(template)
            
        template = _include_re.sub(replace_include, template)

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
        if not self.server:
            self.server = bottle.Bottle()
            
        app = self.server
        
        @app.get('')    
        @app.get('/')
        def index():
            for file in ['index.tml', 'index.tmd', 'index.html']:
                if os.path.exists( os.path.join(self.root, file) ):
                    return serve(file)
                    
            bottle.abort(404)

        def check(path):
            filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))  
            if not filename.startswith(root): 
                raise HTTPError(403, "Access denied.") 
            if not os.path.exists(filename) or not os.path.isfile(filename): 
                raise HTTPError(404, "File does not exist.") 
            if not os.access(filename, os.R_OK): 
                raise HTTPError(403, "You do not have permission to access this file.") 

        @app.get('<path:path>')
        def serve(path):
            check(path)
            if path.endswith('.tml') or path.endswith('.tmd'):
                params = bottle.request.params
                return self.render(path, **params)
            if os.path.isdir( os.path.join(self.root, path) ):
                pass
            else:
                return bottle.static_file(path, root=self.root)
            
        app.run(**kwargs)
