#!/usr/bin/env python
# Created:  Thu 19 Mar 2015
# Modified: Mon 17 Aug 2015
# Author:   Josh Wainwright
# Filename: times-summarise.py

import sys, time, os
from os.path import expanduser
from math import floor

dates = []
dstarts = []
lstarts = []
lends = []
dends = []
s = ''


## start function secs2ts
# Convert a number of seconds to timestamp format HH:MM.
def secs2ts(s):
    s = int(s)
    return '{:0>2}:{:0>2}'.format(int(floor(s / 3600)), int((s % 3600) / 60))
## end function secs2ts


## start function str2secs
# Convert a timestamp format HHMMSS to a number of seconds.
def str2secs(s):
    return int(s[0:2]) * 3600 + int(s[2:4]) * 60 + int(s[4:6])
## end function str2secs


## start function s2h
# Convert a number of seconds to a number of hours.
def s2h(s):
    return (float(s) / 60) / 60
## end function s2h


## start function readdata
def readdata(infile):
    for line in infile:
        if line.startswith('#') or 'w' in line or line.strip() == '':
            continue

        columns = line.split(',')
        columns = [c.strip() for c in columns]

        try:
            dates.append(columns[0])
            dstarts.append(str2secs(columns[1]))
            lstarts.append(str2secs(columns[2]))
            lends.append(str2secs(columns[3]))
            dends.append(str2secs(columns[4]))
        except:
            pass
## end function readdata


## start function updatefile
def updatefile(infile):
    writefile = open('times.tmp', 'w')
    replace = True
    monthstart = 0
    monthend = 0
    lnum = 0
    for line in infile:
        line = line.rstrip()
        if line.startswith('#:'):
            print(line)

        if line.startswith('#: Date'):
            month_old = int(line.split('-')[1])
            month_cur = int(time.strftime('%m'))
            if (month_cur - month_old) % 12 < -2:
                replace = False
            else:
                line = "#: Date:  " + time.strftime("%Y-%m-%d")
                global s
            month_old = '01'
        if line.startswith('#: ') and replace:
            if line.startswith('#: Range'):
                line = "#: Range:   " + str(s.dayrange).rjust(6)
            elif line.startswith('#: Day'):
                line = "#: Day:     " + s.avdstart.rjust(6) + " -> " + s.avdend
            elif line.startswith('#: Lunch'):
                line = "#: Lunch:   " + s.avlstart.rjust(6) + " -> " + s.avlend
            elif line.startswith('#: Hours D'):
                line = "#: Hours D: " + s.avdhours.rjust(6)
            elif line.startswith('#: Hours W'):
                line = "#: Hours W: " + s.avwhours.rjust(6)
            elif line.startswith('#: Hours L'):
                line = "#: Hours L: " + s.avlhours.rjust(6)
            elif line.startswith('#: Sal w/d/h'):
                line = '#: ' + strav[7]
                strav.append(
                    "Sal wdh:  {:.0f} {:.0f} {:.2f}".format(
                        s.salweek, s.salday, s.salhour))
        elif line.startswith('## '):
            continue
        elif not line or line.startswith('#'):
            pass
        else:
            if not 'w' in line:
                lnum += 1

            month_cur = line.split(',')[0][4:6]
            if not month_cur == month_old:
                month_old = month_cur
                monthend = lnum
                m = calcrange(monthstart, monthend)
                line = '## {} {}, {}, {}, {}\n{}'.format(m.dayrange,
                                                         m.avdstart,
                                                         m.avlstart, m.avlend,
                                                         m.avdend, line)
                monthstart = monthend

        writefile.write(line + '\n')
    writefile.close()
    os.rename(writefile.name, infile.name)
    print('')
    ## end function updatefile


    ## start function calcall
def calcall():
    return calcrange(0, len(dstarts))
## end function calcall


## start function calcrange
def calcrange(s, e):
    if s < 0:
        s = len(dstarts) + s
    if e < 0:
        e = len(dstarts)
    dayrange = len(dstarts[s:e])
    avdstart = sum(dstarts[s:e]) / len(dstarts[s:e])
    avlstart = sum(lstarts[s:e]) / len(lstarts[s:e])
    avlend = sum(lends[s:e]) / len(lends[s:e])
    avdend = sum(dends[s:e]) / len(dends[s:e])

    avdhours = secs2ts(avdend - avdstart)
    avwhours = secs2ts(((avdend - avdstart) - (avlend - avlstart)) * 5)
    avlhours = secs2ts(avlend - avlstart)[-5:]

    salyear = 26512
    salweek = salyear / (52 - 5)
    salday = salweek / 5
    salhour = salday / s2h(avdend - avdstart)

    avdstart = secs2ts(avdstart)
    avlstart = secs2ts(avlstart)
    avlend = secs2ts(avlend)
    avdend = secs2ts(avdend)

    return Averages(dayrange, avdstart, avlstart, avlend, avdend, avdhours,
                    avwhours, avlhours, salweek, salday, salhour)
## end function calcrange


## start class Averages
class Averages:
    def __init__(self, dayrange, avdstart, avlstart, avlend, avdend, avdhours,
                 avwhours, avlhours, salweek, salday, salhour):
        self.dayrange = dayrange
        self.avdstart = avdstart
        self.avlstart = avlstart
        self.avlend = avlend
        self.avdend = avdend
        self.avdhours = avdhours
        self.avwhours = avwhours
        self.avlhours = avlhours
        self.salweek = salweek
        self.salday = salday
        self.salhour = salhour

    def printstr(self):
        return """   Date: {}
   Range: {:8}
   Day: {:>10} -> {}
   Lunch: {:>8} -> {}
   Hours D: {:>6}
   Hours W: {:>6}
   Hours L: {:>6}
   Sal wdh: {} {} {:.2f}""".format(time.strftime('%Y-%m-%d'), self.dayrange,
       self.avdstart, self.avdend, self.avlstart, self.avlend, self.avdhours,
       self.avwhours, self.avlhours, self.salweek, self.salday, self.salhour)
## end class Averages


## start function main
def main(argv):
    infile = open(expanduser('~') + '/Documents/Details/times/times.txt')
    readdata(infile)
    global s

    if len(argv) > 0 and argv[0].startswith('-r'):
        start, end = argv[0].lstrip('-r').split(':')
        if not start:
            start = 0
        if not end:
            end = -1
        if end < start:
            start, end = end, start
        s = calcrange(int(start), int(end))

    elif len(argv) > 0 and argv[0].startswith('-b'):
        opt = argv[0]
        back = opt.lstrip('-b')
        s = calcrange(0 - int(back), -1)

    elif len(argv) > 0 and argv[0] == '-n':
        s = calcall()

    else:
        s = calcall()
        infile.seek(0)
        updatefile(infile)
        infile.close()

    print(s.printstr())
## end function main

if __name__ == '__main__':
    main(sys.argv[1:])
