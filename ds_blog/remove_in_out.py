#!/usr/bin/python

import re
import os

re_out = re.compile('Out\s*\[\s*[0-9]*\]:')
re_in1 = re.compile('In\s*\[\s*[0-9]*\]:')
re_in2 = re.compile('In\s*(\xc2\xa0)*\[(\xc2\xa0)*\s*[0-9]*\]:')


def remove_in_out(fname):
    f = open(fname)
    s = f.read()
    s = re_in1.sub('', s)
    s = re_in2.sub('', s)
    s = re_out.sub('', s)

    fout = open(fname, 'w')
    fout.write(s)
    fout.close()


for fname in os.listdir('.'):
    if fname.endswith('.html'):
        remove_in_out(fname)


