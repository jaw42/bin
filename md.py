#!/usr/bin/env python
# Created:  Thu 28 May 2015
# Modified: Wed 10 Jun 2015
# Author:   Josh Wainwright
# Filename: md.py

import os, sys, getopt, tempfile, re
from subprocess import Popen, PIPE, STDOUT

mdopts = '-S'
toc = False
song = False
cssfile = os.path.dirname(os.path.realpath(__file__)) + '/cssfile.css'
inputfiles = []

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
"""
    print(helptext)

# start function cleanfile
def cleanfile(mdfile):
    with open(mdfile, 'r') as inp:
        mdcontents = inp.read()

    mdcontentstmp = []
    for line in mdcontents.split('\n'):
        line = re.sub('(\[.*\])(.*)\.md\)', '\g<1>\g<2>.html)', line)
        if line.startswith('~ '):
            line = '<br/>' + line[2:]
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
    mdcontents = cleanfile(mdfile)
    mdcmd = 'markdown {}'.format(mdopts, mdcontents)
    p = Popen(['markdown', mdopts], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    mdcmdoutput = p.communicate(input=mdcontents)[0]

    try:
        with open(cssfile, 'r') as cssin:
            csscontent = cssin.read()
    except:
        csscontent = ''

    with open(htmlfile, 'w') as htmlout:
        htmlout.write(csscontent)
        htmlout.write(mdcmdoutput)
        htmlout.write('</body>\n</html>\n')
# end function domarkdown

# start function main
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'htp:c:o:s', ['help', 'toc', 'path=', 'cssfile=', 'output=', 'song'])
    except getopt.GetoptError as opterr:
        print(str(opterr))

    htmlpath = ''
    global toc
    global song
    global mdopts
    global cssfile
    global inputfiles
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(1)
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
                song = True

        print('{} -> {} ({})'.format(mdfile, htmlfile, song))
        domarkdown(mdfile, htmlfile)
# end function main

if __name__ == '__main__':
    main(sys.argv[1:])
