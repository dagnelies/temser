########################################
# Generates static pages for themes
########################################

import temser
import os
import os.path

all_themes = []
for subdir in os.listdir('themes/boostwatch'):
    if os.path.isdir('themes/boostwatch/' + subdir):
        all_themes.append({'label':subdir, 'url':subdir+'.html'})


for subdir in os.listdir('themes/boostwatch'):
    print(subdir)
    if os.path.isdir('themes/boostwatch/' + subdir):
        theme = {
            'path': 'themes/boostwatch',
            'flavor': subdir,
            'title': subdir,
            'menu': [{
                'label': 'Themes',
                'children': all_themes
            }]
        }
        temser.apply(root='.', source='site/themes/index.tmd', target='site/themes/' + subdir + '.html', theme=theme)
