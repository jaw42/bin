#!/bin/python
# Created:  Wed 22 Apr 2015
# Modified: Thu 23 Apr 2015
# Author:   Josh Wainwright
# Filename: splitbible.py

import sys, os

if not len(sys.argv) == 3:
    print("Wrong number of arguments")
    print(sys.argv[0] + " bible dir")
    sys.exit(1)

inputfile = sys.argv[1]
newfolder = sys.argv[2]
if not os.path.exists(newfolder):
    os.makedirs(newfolder)

i = 0
outfile = newfolder + "/bible"
out = open(outfile, 'a')
bibfile = newfolder + ".list"
if os.path.exists(bibfile):
    os.remove(bibfile)
bib = open(bibfile, 'a')

with open(inputfile) as f:
    for line in f:
        line = line.replace('\t', '    ')

        if line[:3] == '###':
            i = i + 1
            i0 = '{:0>2}'.format(i)
            tmp = line[4:].replace(' ', '_').rstrip()
            outfile = '{}/{}_{}.bible'.format(newfolder, i0, tmp)

            if os.path.exists(outfile):
                os.remove(outfile)

            out = open(outfile, 'a')
            bib.write(outfile + '\n')
            print(outfile)

        out.write(line)
