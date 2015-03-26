#!/usr/bin/env python
# Created:  Thu 19 Mar 2015
# Modified: Mon 23 Mar 2015
# Author:   Josh Wainwright
# Filename: times-summarise.py

import os
from os.path import expanduser

def loop():
	retval   = []
	total    = [0] * 5
	length   = [0] * 5
	t_total  = [0] * 5
	t_length = [0] * 5
	lnum = 0
	prevmonth = '01'
	for line in lines:
		if line == '\n' or line.startswith('#'): continue

		lnum += 1
		cols = line.split(', ')
		month = cols[0][4:6]
		year = cols[0][:4]
		if day != prevday:
		if month != prevmonth:
			global addedlines
			length = [ l+1 if l==0 else l for l in length ]
			addedlines.append([lnum, "## " + str(length[1]).rjust(2) + " " +\
					secs2ts(total[1]/length[1]) + ", " + \
					secs2ts(total[2]/length[2]) + ", " + \
					secs2ts(total[3]/length[3]) + ", " + \
					secs2ts(total[4]/length[4])])
			total  = [0] * 5
			length = [0] * 5
		prevmonth = month

		for i in range(1,5):
			try:
				ts = cols[i]
				total[i]    += int(str2secs(ts))
				t_total[i]  += int(str2secs(ts))
				length[i]   += 1
				t_length[i] += 1
			except: IndexError

	retval.append(t_length[1])
	for i in range(1,5):
		retval.append(t_total[i] / t_length[i])
	return retval

def secs2ts(s):
	return '{:0>2}:{:0>2}:{:0>2}'.format(s/3600, (s%3600)/60, s%60)

def str2secs(a):
	return int(a[0:2])*3600 + int(a[2:4])*60 + int(a[4:6])

def updatefile():
	lnum = 0
	for line in lines:
		if line == '\n': pass
		elif line.startswith('#: Day Range'  ) : line = '#: ' + strav[0] + '\n'
		elif line.startswith('#: Arrive'     ) : line = '#: ' + strav[1] + '\n'
		elif line.startswith('#: Lunch Start') : line = '#: ' + strav[2] + '\n'
		elif line.startswith('#: Lunch End'  ) : line = '#: ' + strav[3] + '\n'
		elif line.startswith('#: Leave'      ) : line = '#: ' + strav[4] + '\n'
		elif line.startswith('#: Working Day') : line = '#: ' + strav[5] + '\n'
		elif line.startswith('#: Lunch Break') : line = '#: ' + strav[6] + '\n'
		elif line.startswith('## '): continue
		elif line.startswith('#'): pass
		else:
			lnum += 1
			try:
				global addedlines
				if lnum == addedlines[0][0]:
					writefile.write(addedlines[0][1] + '\n')
					addedlines.pop(0)
			except: IndexError

		writefile.write(line)

	writefile.close()
	os.rename(writefile.name, readfile.name)

readfile = open(expanduser('~') + '/Documents/Details/times.txt')
writefile = open('times.txt.tmp', 'w')
lines = readfile.readlines()
addedlines = []

av = loop()
av.append(secs2ts(av[4] - av[1])[-7:])
av.append(secs2ts(av[3] - av[2])[-5:])

strav = []
strav.append("Day Range   " +     str(av[0]).rjust(10))
strav.append("Arrive      " + secs2ts(av[1]).rjust(10))
strav.append("Lunch Start " + secs2ts(av[2]).rjust(10))
strav.append("Lunch End   " + secs2ts(av[3]).rjust(10))
strav.append("Leave       " + secs2ts(av[4]).rjust(10))
strav.append("Working Day " +          av[5].rjust(10))
strav.append("Lunch Break " +          av[6].rjust(10))

for i in range(0, 7):
	print(strav[i])

updatefile()
