#!/usr/bin/env python
# Created:  Thu 19 Mar 2015
# Modified: Mon 20 Apr 2015
# Author:   Josh Wainwright
# Filename: times-summarise.py

import os
import time
from os.path import expanduser


# The main loop, goes through data file and keeps a total of each column.
def loop():

    # Initialise arrays to empty
    retval = []
    total = [0] * 5
    length = [0] * 5
    t_total = [0] * 5
    t_length = [0] * 5
    lnum = 0
    prevmonth = '01'
    for line in lines:

        # Reading the file results in lines that only contain newline
        # ignore these and comments.
        if line == '\n' or line.startswith('#'): continue

        lnum += 1

        # Columns are: Date | day start | lunch start | lunch end | day end
        cols = line.split(', ')
        month = cols[0][4:6]
        year = cols[0][:4]

        # The cur and prev value will be different if the month changed
        if month != prevmonth:
            global addedlines

            # For array increase 0 to 1 to avoid div by 0 errors.
            length = [l + 1 if l == 0 else l for l in length]

            # Keep an array of lines that will be added at the end of each
            # month. Referenced with the line number of non comments only.
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
        # Try since the last line is likely not finished so there will be fewer
        # columns in that line, hence an IndexError
        for i in range(1, 5):
            try:
                ts = cols[i]
                total[i] += int(str2secs(ts))
                t_total[i] += int(str2secs(ts))
                length[i] += 1
                t_length[i] += 1
            except (IndexError, ValueError):
                break

    # Return value - contains the information. First value
    retval.append(t_length[1])
    for i in range(1, 5):
        retval.append(t_total[i] / t_length[i])
    return retval


# Convert a number of seconds to timestamp format HH:MM:SS.
def secs2ts(s):
    return '{:0>2}:{:0>2}:{:0>2}'.format(s / 3600, (s % 3600) / 60, s % 60)


# Convert a timestamp format HHMMSS to a number of seconds.
def str2secs(a):
    return int(a[0:2]) * 3600 + int(a[2:4]) * 60 + int(a[4:6])


# Convert a number of seconds to a number of hours.
def s2h(a):
    return a * 0.000278


# Write the results back to the file.
def updatefile():
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
        elif line == '\n':
            pass
        elif line.startswith('#'):
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
writefile = open('times.txt.tmp', 'w')
lines = readfile.readlines()
addedlines = []

av = loop()  # 0-4
av.append(secs2ts(av[4] - av[1])[-7:])  # 5
av.append(secs2ts((av[4] - av[1]) * 5))  # 6
av.append(secs2ts(av[3] - av[2])[-5:])  # 7

sal_year = 26000
sal_week = sal_year / (52 - 5)
sal_day = sal_week / 5
sal_hour = sal_day / s2h(av[4] - av[1])

for i in range(1, 5):
    av[i] = secs2ts(av[i])

strav = []
strav.append("Date   " + time.strftime("%Y-%m-%d"))
strav.append("Range    " + str(av[0]).rjust(8))
strav.append("Day      " + av[1] + " -> " + av[4])
strav.append("Lunch    " + av[2] + " -> " + av[3])
strav.append("Hours D  " + av[5].rjust(8))
strav.append("Hours W  " + av[6])
strav.append("Hours L  " + av[7].rjust(8))
strav.append(
    "Sal w/d/h {:7.2f} / {:.2f} / {:.2f}".format(sal_week, sal_day, sal_hour))

if printexisting:
    updatefile()
    print("")

for i in range(0, 8):
    print("  " + strav[i])
