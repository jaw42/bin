#!/usr/bin/python

import urllib, os, sys, commands

os.system('firefox' + commands.mkarg(
  'http://www.google.com/search?q='
  + urllib.quote_plus(' '.join(sys.argv[1:]))
  + '+site%3Ajava.sun.com+inurl%3Ajavase%2F6%2Fdocs%2Fapi&btnI=')
  + ' &')
