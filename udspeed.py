#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2012-2014 Matt Martz
# All Rights Reserved.
#
__version__ = '0.2.7'

# Some global variables we use
shutdown_event = None

import math
import time
import os
import sys
import threading
import signal
import time
import datetime

import xml.etree.cElementTree as ET
from urllib2 import urlopen, Request, HTTPError, URLError
from Queue import Queue
from argparse import ArgumentParser as ArgParser

def distance(origin, destination):
    """Determine distance between 2 sets of [lat,lon] in km"""

    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2)
         * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

class FileGetter(threading.Thread):
    """Thread class for retrieving a URL"""

    def __init__(self, url, start):
        self.url = url
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def run(self):
        self.result = [0]
        try:
            if (time.time() - self.starttime) <= 10:
                f = urlopen(self.url)
                while 1 and not shutdown_event.isSet():
                    self.result.append(len(f.read(10240)))
                    if self.result[-1] == 0:
                        break
                f.close()
        except IOError:
            pass

def downloadSpeed(files, quiet=False):
    """Function to launch FileGetter threads and calculate download speeds"""

    start = time.time()

    def producer(q, files):
        for file in files:
            thread = FileGetter(file, start)
            thread.start()
            q.put(thread, True)
            if not quiet and not shutdown_event.isSet():
                sys.stdout.write('.')
                sys.stdout.flush()

    finished = []

    def consumer(q, total_files):
        while len(finished) < total_files:
            thread = q.get(True)
            while thread.isAlive():
                thread.join(timeout=0.1)
            finished.append(sum(thread.result))
            del thread

    q = Queue(6)
    prod_thread = threading.Thread(target=producer, args=(q, files))
    cons_thread = threading.Thread(target=consumer, args=(q, len(files)))
    start = time.time()
    prod_thread.start()
    cons_thread.start()
    while prod_thread.isAlive():
        prod_thread.join(timeout=0.1)
    while cons_thread.isAlive():
        cons_thread.join(timeout=0.1)
    return (sum(finished) / (time.time() - start))

class FilePutter(threading.Thread):
    """Thread class for putting a URL"""

    def __init__(self, url, start, size):
        self.url = url
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        data = chars * (int(round(int(size) / 36.0)))
        self.data = ('content1=%s' % data[0:int(size) - 9]).encode()
        del data
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def run(self):
        try:
            if ((time.time() - self.starttime) <= 10 and
                    not shutdown_event.isSet()):
                f = urlopen(self.url, self.data)
                f.read(11)
                f.close()
                self.result = len(self.data)
            else:
                self.result = 0
        except IOError:
            self.result = 0

def uploadSpeed(url, sizes, quiet=False):
    """Function to launch FilePutter threads and calculate upload speeds"""

    start = time.time()

    def producer(q, sizes):
        for size in sizes:
            thread = FilePutter(url, start, size)
            thread.start()
            q.put(thread, True)
            if not quiet and not shutdown_event.isSet():
                sys.stdout.write('.')
                sys.stdout.flush()

    finished = []

    def consumer(q, total_sizes):
        while len(finished) < total_sizes:
            thread = q.get(True)
            while thread.isAlive():
                thread.join(timeout=0.1)
            finished.append(thread.result)
            del thread

    q = Queue(6)
    prod_thread = threading.Thread(target=producer, args=(q, sizes))
    cons_thread = threading.Thread(target=consumer, args=(q, len(sizes)))
    start = time.time()
    prod_thread.start()
    cons_thread.start()
    while prod_thread.isAlive():
        prod_thread.join(timeout=0.1)
    while cons_thread.isAlive():
        cons_thread.join(timeout=0.1)
    return (sum(finished) / (time.time() - start))

def getAttributesByTagName(dom, tagName):
    """Retrieve an attribute from an XML document and return it in a
   consistent format

   Only used with xml.dom.minidom, which is likely only to be used
   with python versions older than 2.5
   """
    elem = dom.getElementsByTagName(tagName)[0]
    return dict(list(elem.attributes.items()))

def getConfig():
    """Download the speedtest.net configuration and return only the data
   we are interested in
   """

    uh = urlopen('http://www.speedtest.net/speedtest-config.php')
    configxml = []
    while 1:
        configxml.append(uh.read(10240))
        if len(configxml[-1]) == 0:
            break
    if int(uh.code) != 200:
        return None
    uh.close()
    try:
        root = ET.fromstring(''.encode().join(configxml))
        config = {
            'client': root.find('client').attrib,
            'times': root.find('times').attrib,
            'download': root.find('download').attrib,
            'upload': root.find('upload').attrib}
    except AttributeError:
        root = DOM.parseString(''.join(configxml))
        config = {
            'client': getAttributesByTagName(root, 'client'),
            'times': getAttributesByTagName(root, 'times'),
            'download': getAttributesByTagName(root, 'download'),
            'upload': getAttributesByTagName(root, 'upload')}
    del root
    del configxml
    return config

def closestServers(client, all=False):
    """Determine the 5 closest speedtest.net servers based on geographic
   distance
   """

    uh = urlopen('http://www.speedtest.net/speedtest-servers.php')
    serversxml = []
    while 1:
        serversxml.append(uh.read(10240))
        if len(serversxml[-1]) == 0:
            break
    if int(uh.code) != 200:
        return None
    uh.close()
    try:
        root = ET.fromstring(''.encode().join(serversxml))
        elements = root.getiterator('server')
    except AttributeError:
        root = DOM.parseString(''.join(serversxml))
        elements = root.getElementsByTagName('server')
    servers = {}
    for server in elements:
        try:
            attrib = server.attrib
        except AttributeError:
            attrib = dict(list(server.attributes.items()))
        d = distance([float(client['lat']), float(client['lon'])],
                     [float(attrib.get('lat')), float(attrib.get('lon'))])
        attrib['d'] = d
        if d not in servers:
            servers[d] = [attrib]
        else:
            servers[d].append(attrib)
    del root
    del serversxml
    del elements

    closest = []
    for d in sorted(servers.keys()):
        for s in servers[d]:
            closest.append(s)
            if len(closest) == 5 and not all:
                break
        else:
            continue
        break

    del servers
    return closest

def getBestServer(servers):
    """Perform a speedtest.net "ping" to determine which speedtest.net
   server has the lowest latency
   """

    results = {}
    for server in servers:
        cum = []
        url = os.path.dirname(server['url'])
        for i in range(0, 3):
            try:
                uh = urlopen('%s/latency.txt' % url)
            except (HTTPError, URLError):
                cum.append(3600)
                continue
            start = time.time()
            text = uh.read(9)
            total = time.time() - start
            if int(uh.code) == 200 and text == 'test=test'.encode():
                cum.append(total)
            else:
                cum.append(3600)
            uh.close()
        avg = round((sum(cum) / 3) * 1000000, 3)
        results[avg] = server

    fastest = sorted(results.keys())[0]
    best = results[fastest]
    best['latency'] = fastest

    return best

def ctrl_c(signum, frame):
    """Catch Ctrl-C key sequence and set a shutdown_event for our threaded
   operations
   """

    global shutdown_event
    shutdown_event.set()
    raise SystemExit('\nCancelling...')

def speedtest():
    """Run the full speedtest.net test"""

    global shutdown_event, source
    shutdown_event = threading.Event()

    signal.signal(signal.SIGINT, ctrl_c)

    description = (
        'Command line interface for testing internet bandwidth using '
        'speedtest.net.\n'
        '------------------------------------------------------------'
        '--------------\n'
        'https://github.com/sivel/speedtest-cli')

    parser = ArgParser(description=description)
    # Give optparse.OptionParser an `add_argument` method for
    # compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass
    parser.add_argument('--bytes', dest='units', action='store_const',
                        const=('bytes', 1), default=('bits', 8),
                        help='Display values in bytes instead of bits.')

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    print('Retrieving speedtest.net configuration...')
    try:
        config = getConfig()
    except URLError:
        print('Cannot retrieve speedtest configuration')
        sys.exit(1)

    servers = closestServers(config['client'])

    print('Testing from %(isp)s (%(ip)s)...' % config['client'])

    print('Selecting best server based on ping...')
    best = getBestServer(servers)

    # Python 2.7 and newer seem to be ok with the resultant encoding
    # from parsing the XML, but older versions have some issues.
    # This block should detect whether we need to encode or not
    try:
        unicode()
        print(('Hosted by %(sponsor)s (%(name)s) [%(d)0.2f km]: '
                '%(latency)s ms' % best).encode('utf-8', 'ignore'))
    except NameError:
        print('Hosted by %(sponsor)s (%(name)s) [%(d)0.2f km]: '
                '%(latency)s ms' % best)

    sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
    urls = []
    for size in sizes:
        for i in range(0, 4):
            urls.append('%s/random%sx%s.jpg' %
                        (os.path.dirname(best['url']), size, size))
    sys.stdout.write('Testing download speed')
    dlspeed = downloadSpeed(urls)
    print('')
    print('Download: %0.2f M%s/s' %
           ((dlspeed / 1000 / 1000) * args.units[1], args.units[0]))

    sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
    sizes = []
    for size in sizesizes:
        for i in range(0, 25):
            sizes.append(size)
    sys.stdout.write('Testing upload speed')
    ulspeed = uploadSpeed(best['url'], sizes)
    print('')
    print('Upload: %0.2f M%s/s' %
           ((ulspeed / 1000 / 1000) * args.units[1], args.units[0]))

######CRAP I AM ADDING

    ping = ('%(latency)s' % best).encode('utf-8', 'ignore')
    print(ping)

    download = round((dlspeed * 8 / 1000 / 1000), 2)
    print(download)

    upload = round((ulspeed * 8 / 1000 / 1000), 2)
    print(upload)

    ts = time.time()

    ds = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    strappend = ds + ',' + ping + ','+  str(download) + ',' + str(upload)
    print(strappend)

    f = open('speedtest.csv','a')
    f.write(strappend + '\n')
    f.close()

def main():
    try:
        speedtest()
    except KeyboardInterrupt:
        print('\nCancelling...')

if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:expandtab
