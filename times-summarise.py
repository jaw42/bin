#!/usr/bin/env python
# Created:  Thu 19 Mar 2015
# Modified: Fri 08 May 2015
# Author:   Josh Wainwright
# Filename: times-summarise.py

import os
import sys
import time
from os.path import expanduser
from math import floor


# The main loop, goes through data file and keeps a total of each column.
def loop():

    # Initialise arrays to empty
    total = [0] * 5
    length = [0] * 5
    t_total = [0] * 5
    t_length = [0] * 5
    lnum = 0
    prevmonth = '01'
    for line in lines:

        # Reading the file results in lines that only contain newline
        # ignore these and comments.
        if line == '\n' or line.startswith('#'):
            continue

        lnum += 1

        # Columns: Date | day start | lunch start | lunch end | day end | hol
        cols = line.split(', ')
        month = cols[0][4:6]

        # The cur and prev value will be different if the month changed
        if month != prevmonth:
            # For array increase 0 to 1 to avoid div by 0 errors.
            length = [l + 1 if l == 0 else l for l in length]

            # Keep an array of lines that will be added at the end of each
            # month. Referenced with the line number of non comments only.
            global addedlines
            addedlines.append([lnum, "## " + str(length[1]).rjust(2) + " " +
                                secs2ts(total[1]/length[1]) + ", " +
                                secs2ts(total[2]/length[2]) + ", " +
                                secs2ts(total[3]/length[3]) + ", " +
                                secs2ts(total[4]/length[4])])

            # Reset values ready for the following month.
            total = [0] * 5
            length = [0] * 5
        prevmonth = month

        # For each of the columns, except date, increment the totals.
        # "IndexError" catches the last line which is likely not complete.
        # "ValueError" catches hols where int('w') is not allowed.
        for i in range(1, 5):
            try:
                secs = int(str2secs(cols[i]))
                total[i] += secs
                t_total[i] += secs
                length[i] += 1
                t_length[i] += 1
            except (IndexError, ValueError):
                break

    # Return value - contains the information. Values are number of days
    # covered, day start. lunch start, lunch end, day end.
    retval = []
    retval.append(t_length[1])
    for i in range(1, 5):
        retval.append(t_total[i] / float(t_length[i]))
    return retval


# Convert a number of seconds to timestamp format HH:MM.
def secs2ts(s):
    s = int(s)
    return '{:0>2}:{:0>2}'.format(int(floor(s / 3600)), int((s % 3600) / 60))


# Convert a timestamp format HHMMSS to a number of seconds.
def str2secs(s):
    return int(s[0:2]) * 3600 + int(s[2:4]) * 60 + int(s[4:6])


# Convert a number of seconds to a number of hours.
def s2h(s):
    return (s / 60) / 60


# Write the results back to the file.
def updatefile():
    writefile = open('times.txt', 'w')
    lnum = 0
    replace = True
    for line in lines:
        global printexisting
        if line.startswith('#:') and printexisting: print(line.rstrip())

        if line.startswith('#: Date'):
            month_old = 0
            try:
                month_old = int(line.split('-')[1])
            except IndexError:
                pass
            month_cur = int(time.strftime('%m'))
            if (month_cur - month_old) % 12 < 2:
                replace = False
            else:
                line = '#: ' + strav[0] + '\n'
        if replace:
            if line.startswith('#: Range'): line = '#: ' + strav[1] + '\n'
            elif line.startswith('#: Day'): line = '#: ' + strav[2] + '\n'
            elif line.startswith('#: Lunch'): line = '#: ' + strav[3] + '\n'
            elif line.startswith('#: Hours D'): line = '#: ' + strav[4] + '\n'
            elif line.startswith('#: Hours W'): line = '#: ' + strav[5] + '\n'
            elif line.startswith('#: Hours L'): line = '#: ' + strav[6] + '\n'
            elif line.startswith('#: Sal w/d/h'):
                line = '#: ' + strav[7] + '\n'
        elif line.startswith('## '):
            continue
        elif line == '\n' or line.startswith('#'):
            pass
        else:
            lnum += 1
            try:
                global addedlines
                if lnum == addedlines[0][0]:
                    writefile.write(addedlines[0][1] + '\n')
                    addedlines.pop(0)
            except IndexError:
                pass

        writefile.write(line)

    writefile.close()
    os.rename(writefile.name, readfile.name)


printexisting = True
if len(sys.argv) > 1 and sys.argv[1] == "-n":
    printexisting = False

readfile = open(expanduser('~') + '/Documents/Details/times/times.txt')
lines = readfile.readlines()
addedlines = []

av = loop()  # 0-4
av.append(secs2ts(av[4] - av[1])[-7:])  # 5
av.append(secs2ts(((av[4] - av[1]) - (av[3] - av[2])) * 5))  # 6 hours week
av.append(secs2ts(av[3] - av[2])[-5:])  # 7

sal_year = 26000
sal_week = sal_year / (52 - 5)
sal_day = sal_week / 5
sal_hour = sal_day / s2h(av[4] - av[1])

for i in range(1, 5):
    av[i] = secs2ts(av[i])

strav = []
strav.append("Date:  " + time.strftime("%Y-%m-%d"))
strav.append("Range:   " + str(av[0]).rjust(6))
strav.append("Day:     " + av[1].rjust(6) + " -> " + av[4])
strav.append("Lunch:   " + av[2].rjust(6) + " -> " + av[3])
strav.append("Hours D: " + av[5].rjust(6))
strav.append("Hours W: " + av[6].rjust(6))
strav.append("Hours L: " + av[7].rjust(6))
strav.append(
        "Sal wdh:  {:.0f} {:.0f} {:.2f}".format(sal_week, sal_day, sal_hour))

if printexisting:
    updatefile()
    print("")

for i in range(0, 8):
    print("  " + strav[i])
