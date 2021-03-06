import temser
import json

#temser.run(debug=True, host='0.0.0.0')

#ts = temser.TemSer(root='./examples', theme={'path': '/theme'})
#print(ts.render('basic/basic.tml', foo='FOO', bar='BAR'))

theme = {
    'path': '/themes/boostwatch',
    'flavor':'cerulean',
    'title': 'QuickPage',
    'menu': [{
        'label':'Intro',
        'url':'index.tmd'
    },{
        'label':'Themes',
        'url':'themes.tmd'
    },{
        'label':'Docs',
        'url':'docs.tmd'
    },{
        'label':'Examples',
        'url':'examples.tmd'
    }]
}
ts = temser.TemSer(root='.', theme=theme)
#print(ts.render('examples/index.tmd'))


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

ts.hooks['@countdown'] = countdown

ts.start(debug=True, host='0.0.0.0')



