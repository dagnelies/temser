########################################
# Generates static pages for themes
########################################

import temser
import os
import os.path

for subdir in os.listdir('themes/boostwatch'):
    print 
    if os.path.isdir('themes/boostwatch/' + subdir):
        temser.apply(root='.', source='examples/index.tmd', target='site/themes/' + subdir + '.html', theme={'path': '/themes/bootswatch', 'flavor': subdir})
