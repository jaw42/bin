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

def s2h(a):
	return a * 0.000278
def updatefile():
	lnum = 0
	for line in lines:
		if line == '\n': pass
		elif line.startswith('#: Range'   ) : line = '#: ' + strav[0] + '\n'
		elif line.startswith('#: Day'     ) : line = '#: ' + strav[1] + '\n'
		elif line.startswith('#: Lunch'   ) : line = '#: ' + strav[2] + '\n'
		elif line.startswith('#: Hours D' ) : line = '#: ' + strav[3] + '\n'
		elif line.startswith('#: Hours W' ) : line = '#: ' + strav[4] + '\n'
		elif line.startswith('#: Hours L' ) : line = '#: ' + strav[5] + '\n'
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

av = loop()                            # 0-4
av.append(secs2ts(av[4] - av[1])[-7:]) # 5
av.append(secs2ts((av[4]-av[1])*5))    # 6
av.append(secs2ts(av[3] - av[2])[-5:]) # 7

sal_year = 26000
sal_week = sal_year / (52-5)
sal_day = sal_week / 5
sal_hour = sal_day / s2h(av[4] - av[1])

for i in range(1,5):
	av[i] = secs2ts(av[i])

strav = []
strav.append("Range    " + str(av[0]).rjust(8))
strav.append("Day      " + av[1].rjust(8) + " -> " + av[4].rjust(8))
strav.append("Lunch    " + av[2].rjust(8) + " -> " + av[3].rjust(8))
strav.append("Hours D  " + av[5].rjust(8))
strav.append("Hours W  " + av[6].rjust(8))
strav.append("Hours L  " + av[7].rjust(8))

for i in range(0, 6):
	print(strav[i])

print("Sal w/d/h %7.2f / %.2f / %.2f" % (sal_week, sal_day, sal_hour))

updatefile()
