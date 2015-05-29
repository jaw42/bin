#!/usr/bin/env python
# Created:  Thu 21 May 2015
# Modified: Thu 28 May 2015
# Author:   Josh Wainwright
# Filename: dwmstatus.py

import sys, time, os, subprocess

tval_before = time.time()
tmpfolder = "/tmp/dwm_status_bar"
arg = ''

LAPTOP = False
DESKTOP = False
VMBOX = True

if LAPTOP:
    interface = 'wlan0'
    diskone = 'sda7'
    wireless = 1
    update = 'pacman'
    mailret = 'curl'
elif DESKTOP:
    interface = 'wlp4s0'
    diskone = 'sda2'
    disktwo = 'sda3'
    disktwolab = 'h'
    wireless = 1
    update = 'pacman'
    mailret = 'mbox'
elif VMBOX:
    interface = 'eth0'
    diskone = 'sda1'
    wireless = 0
    update = 'aptget'
    mailret = 'curl'


# start function mpd
def mpd():
    testTimeNow(0, 'mpd', arg)
    mpcstatus = subprocess.check_output('mpc status'.split())
    stat = substring(mpcstatus, '[', ']')
    stat_short = ''

    if stat:
        if 'playing' in stat:
            stat_short = '>'
        elif 'paused' in stat:
            stat_short = '||'

        curMessy = subprocess.check_output(
            'mpc current -f "[[%artist% - ]%title%]|[%file%]" 2> /dev/null| head -n 1')
        cur = curMessy.strip()
        perc = substring(mpcstatus, '(', ')')
        perc = perc.strip()

        with open(tmpfolder + '/mpd') as mpdfile:
            mpdfile.write(' \x08' + stat_short + perc + ' ' + cur + '\x01')
# end function mpd


# start function opn
def opn():
    if testTimeNow(600, 'open', arg):
        try:
            opn_num = subprocess.check_output('lsof').count('\n')
            with open(tmpfolder + '/open') as openfile:
                openfile.write(' ' + str(opn_num))
        except:
            pass
# end function opn


# start function pac
def pac():
    if testTimeNow(120, 'pac', arg):
        if 'pacman' in update:
            pacup = subprocess.check_output('pacman -Qqu').count('\n')
        elif 'aptget' in update:
            pacup = subprocess.check_output(
                '/usr/lib/update-notifier/apt-check'.split(),
                stderr=subprocess.STDOUT)
            if len(pacup) >= 3:
                pacup = int(pacup.split(';')[0])

        with open(tmpfolder + '/pac', 'w') as pacfile:
            if pacup > 0:
                pacfile.write(' \x04[P] \x01' + str(pacup))
            else:
                pacfile.write('')
# end function pac


# start function mail
def mail():
    if testTimeNow(120, 'mail', arg):
        with open(tmpfolder + '/mail', 'w') as mailfile:
            if 'curl' in mailret:
                feed = subprocess.check_output(
                    'curl -n --silent "https://mail.google.com/mail/feed/atom"',
                    shell=True)

                if 'fullcount' in feed:
                    newNum = substring(feed, '<fullcount>', '</fullcount>')

                    if not newNum == '0':
                        mailfile.write(' \x04[M] \x01' + newNum)
                    else:
                        mailfile.write('')
                else:
                    mailfile.write('')
            elif 'mbox' in mailret:
                number = subprocess.check_output(
                    'find ~/mail/gmail/INBOX -type f | grep -vE ",[^,]*S[^,]*$"').count('\n')
                if number > 0:
                    mailfile.write(' \x04[M] \x01' + number)
                else:
                    mailfile.write('')
# end function mail


# start function hddhelper
def hddhelper(diskn):
    output = subprocess.check_output(
        'df /dev/{} --output=pcent'.format(diskn).split())
    return output.split('\n')[1].strip()
# end function hddhelper


# start function hdd
def hdd():
    if testTimeNow(600, 'hdd', arg):
        disk1 = hddhelper(diskone)

        with open(tmpfolder + '/hdd', 'w') as hddfile:
            hddfile.write(' \x06[H] \x01/ ' + disk1)
# end function hdd


# start function ipa
def ipa():
    if testTimeNow(3600, 'ipa', arg):
        ipcmd = 'ip addr show dev ' + interface
        ipout = subprocess.check_output(ipcmd.split())

        for line in ipout.split('\n'):
            if 'inet' in line:
                ipaddr = line.strip().split(' ')[1]
                break

        with open(tmpfolder + '/ipa', 'w') as ipafile:
            ipafile.write(' \x06[I] \x01' + ipaddr)
# end function ipa


# start function net
def net():
    if wireless:
        if testTimeNow(600, 'net', arg):
            for line in open('/proc/net/wireless', 'r'):
                if interface in line:
                    # TODO
                    signaltmp = ''
                    break

            if int(signaltmp) < 30:
                signal = '\x07' + signaltmp + '%\x01'
            else:
                signal = signaltmp + '%'

            with open(tmpfolder + '/net', 'w') as netfile:
                netfile.write(' \x06[W] \x01' + signal)
# end function net


# start function dte
def dte():
    testTimeNow(0, 'date', arg)
    with open('/proc/uptime', 'r') as upfile:
        seconds = float(upfile.read().split()[0])

    minutes = seconds / 60 % 60
    hours = seconds / 60 / 60 % 24
    days = seconds / 60 / 60 / 24

    if hours == 0:
        uptime = str(minutes) + 'm '
    elif days == 0:
        uptime = str(hours) + 'h ' + str(minutes) + 'm '
    elif days > 10:
        uptime = '\x03{}d \x01{}h {}m'.format(str(days), str(hours),
                                              str(minutes))
    else:
        uptime = '{}d {}h {}m'.format(str(days), str(hours), str(minutes))

    timedate_now = time.strftime('%I:%M:%S%p \x01 %d %b\'%y')

    with open(tmpfolder + '/dte', 'w') as dtefile:
        dtefile.write(' \x06[Up] \x01' + uptime + ' \x08' + timedate_now)
# end function dte


# start function checkFolders
def checkFolders():
    if not os.path.exists(tmpfolder):
        os.makedirs(tmpfolder)
# end function checkFolders


# start function concatenate
def concatenate():
    filenames = ['mpd', 'open', 'pac', 'mail', 'hdd', 'ipa', 'net', 'dte']
    with open(tmpfolder + '/content', 'w') as outfile:
        for fname in filenames:
            try:
                with open(tmpfolder + '/' + fname) as infile:
                    outfile.write(infile.read())
            except:
                pass
# end function concatenate


# start function testTimeNow
def testTimeNow(duration, prog, arg):
    global tval_after
    global tval_before

    tval_after = time.time()
    tval_result = tval_after - tval_before
    print('\t:{}'.format(tval_result))
    tval_before = time.time()

    if duration == 0 or 'now' in arg:
        sys.stdout.write('{:<5}'.format(prog))
        return True

    current = time.time() % duration
    print('{}\t{}\t{}'.format(prog, duration, current))

    if current > 0 and current < 11:
        return True

    return False
# end function testTimeNow


# start function substring
def substring(string, start_str, end_str):
    try:
        start_idx = string.index(start_str) + len(start_str) - 1
        end_idx = string.index(end_str)
        return string[start_idx + 1:end_idx]
    except:
        return ''
# end function substring


# start function main
def main(args):

    global arg
    if len(args) == 1:
        arg = args[0]

    mpd()
    opn()
    pac()
    mail()
    hdd()
    ipa()
    net()
    dte()

    global tval_after
    global tval_before
    tval_after = time.time()
    tval_result = tval_after - tval_before
    print('\t:{}\n'.format(tval_result))

    checkFolders()
    concatenate()


if __name__ == '__main__':
    main(sys.argv[1:])
