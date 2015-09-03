#!/usr/bin/env python
# Created:  Thu 28 May 2015
# Modified: Thu 03 Sep 2015
# Author:   Josh Wainwright
# Filename: md.py

import os, sys, getopt, tempfile, re
from subprocess import Popen, PIPE, STDOUT

verbose = False
mdopts = '-S'
toc = False
song = False
basedir = ''
inputfiles = []

# start function verboseprint
def verboseprint(msg):
    if verbose:
        print(msg)
# end function verboseprint

# start function usage
def usage():
    helptext = """md.py [-hts] [-p PATH] [-c CSSFILE] [-o OUTPUT] FILE

    -h, --help  Show this help text
    -t, --toc   Include a table of contents in generated html output
    -s, --song  Format the html as a song or poem (likely to be removed)
    -p PATH, --path=PATH
                Use the value of PATH as the location to place the html file
    -c CSSFILE, --css=CSSFILE
                Use CSSFILE as the css for the generated html file
    -o OUTPUT, --output=OUTPUT
                Put the generated html into the file called OUTPUT.
    -b BASEDIR, --basedir=BASEDIR
                Use the specified directory as the base for link references.
"""
    print(helptext)

# start function cleanfile
def cleanfile(mdfile):
    with open(mdfile, 'r') as inp:
        mdcontents = inp.read()

    mdcontentstmp = []
    for line in mdcontents.split('\n'):

        # Replace .md links with .html
        line = re.sub('(\[.*\])(.*)\.md\)', '\g<1>\g<2>.html)', line)

        # Use ~ at start of line for poems
        if line.startswith('~ '):
            line = '<br/>' + line[2:]
        if line.startswith('> ~ '):
            line = '> <br/>' + line[4:]

        mdcontentstmp.append(line)
    mdcontents = '\n'.join(mdcontentstmp)

    mdcontents = ifsong(mdcontents)

    return mdcontents
# end function cleanfile

# start function ifsong
def ifsong(content):
    global song
    if song:
        newcontent = []
        for line in content.split('\n\n'):
            newcontent.append('\n\n' + line.replace('\n', '\n<br/>'))

        return ''.join(newcontent)
    return content
# end function ifsong

# start function domarkdown
def domarkdown(mdfile, htmlfile):
    global mdopts
    if sys.version_info >= (3, 0):
        mdcontents = cleanfile(mdfile).encode('utf8')
        p = Popen(['markdown'] + mdopts.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        mdcmdoutput = p.communicate(input=mdcontents)[0]
        mdcmdoutput = mdcmdoutput.decode('utf8')
    else:
        mdcontents = cleanfile(mdfile)
        p = Popen(['markdown'] + mdopts.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        mdcmdoutput = p.communicate(input=mdcontents)[0]

    try:
        with open(cssfile, 'r') as cssin:
            csscontent = cssin.read()
    except:
        global basedir
        csscontent = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
<title>markdown to html</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="{0}res/css.css"/>
<link rel="stylesheet" type="text/css" href="/res/css.css"/>
<script src="{0}res/sorttable.js"></script>
<script src="/res/sorttable.js"></script>
""".format(basedir)

    htmlcontent = []
    for line in mdcmdoutput.split('\n'):
        line = line.replace('<table>', '<table class="sortable">')
        htmlcontent.append(line)

    with open(htmlfile, 'w') as htmlout:
        htmlout.write(csscontent)
        htmlout.write('\n'.join(htmlcontent))
        htmlout.write('</body>\n</html>\n')
# end function domarkdown

# start function main
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'htp:c:o:sb:', ['help', 'toc', 'path=', 'cssfile=', 'output=', 'song', 'basedir='])
    except getopt.GetoptError as opterr:
        print(str(opterr))

    htmlpath = ''
    global toc
    global song
    global mdopts
    global cssfile
    global inputfiles
    global basedir
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(1)
        if opt in ('-v', '--verbose'):
            verbose = True
        if opt in ('-p', '--path'):
            htmlpath = arg
        elif opt in ('-o', '--output'):
            htmlfile = arg
        elif opt in ('-t', '--toc'):
            toc = True
            mdopts = mdopts + ' -f toc -T'
        elif opt in ('-s', '--song'):
            song = True
        elif opt in ('-c', '--cssfile'):
            cssfile = arg
        elif opt in ('-b', '--basedir'):
            basedir = arg
            basedir = basedir.replace('/cygdrive/c', '')
        else:
            assert False, "unknown option"

    inputfiles = args

    for mdfile in inputfiles:
        if htmlpath:
            if '.md' in mdfile:
                htmlfile = htmlpath + '/' + mdfile.replace('.md', '.html')
            else:
                htmlfile = htmlpath + '/' + mdfile + '.html'
        else:
            if '.md' in mdfile:
                htmlfile = mdfile.replace('.md', '.html')
            else:
                htmlfile = mdfile + '.html'

        if 'Song' in htmlfile or 'Poem' in htmlfile:
            if not 'index' in htmlfile:
                verboseprint('Song = True')
                song = True

        verboseprint('{} -> {}'.format(mdfile, htmlfile))
        domarkdown(mdfile, htmlfile)
# end function main

if __name__ == '__main__':
    main(sys.argv[1:])
