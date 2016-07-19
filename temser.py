import bottle
import barmaid
import os
import os.path

ROOT='examples'
app = bottle.Bottle()
maid = barmaid.Barmaid(root=ROOT)

def exists(path):
    return os.path.exists(ROOT + os.sep + path)
@app.get('/')
def index():
    for file in ['index.tml', 'index.html']:
        if exists(file):
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
