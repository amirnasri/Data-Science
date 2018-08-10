#!/usr/bin/python

import re
import os

ipynb_meta = [re.findall('(.*).ipynb-meta', f) for f in os.listdir('content')]
files = [f[0] for f in ipynb_meta if len(f) != 0 and os.path.isfile('content/%s.ipynb' % f[0])]
files = ['-'.join(f.split('_')) for f in files]

for f in files:
    print 'cp output/%s.html ../../amirnasri.github.io/' % f
    os.system('cp output/%s.html ../../amirnasri.github.io/' % f)
