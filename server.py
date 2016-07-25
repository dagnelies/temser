import bottle
import barmaid
import os
import os.path
import json

ROOT = 'examples'
app  = bottle.Bottle()
maid = barmaid.Barmaid(root=ROOT)

def exists(path):
    return os.path.exists(os.path.join(ROOT,path))
    
@app.get('/')
def index():
    for file in ['index.tml', 'index.html']:
        if os.path.exists( os.path.join(ROOT,file) ):
            return serve(file)
            
    bottle.abort(404)

@app.get('/<path:path>')
def serve(path):
    if path.endswith('.tml'):
        params = bottle.request.params
        return maid.mix(path, **params)
    else:
        return bottle.static_file(path, root=ROOT)
    
if __name__ == "__main__":
    app.run(debug=True, reloader=True, host='0.0.0.0')
