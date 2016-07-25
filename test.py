import server
import json


# To JSON or not?
def countdown(path, parsed):
    tokens = path.strip('/').split('/')
    if len(tokens) < 2:
        return [0]
    assert len(tokens) == 2 and tokens[0] == '@countdown'
    n = int(tokens[-1])
    res = list(range(n,0,-1))
    if parsed:
        return res
    else:
        return json.dumps(res)

server.maid.hooks['@countdown'] = countdown

server.app.run(debug=True, reloader=True, host='0.0.0.0')

