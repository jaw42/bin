#!/usr/bin/python
# Created:  Wed 29 Apr 2015
# Modified: Thu 04 Jun 2015
# Author:   Josh Wainwright
# Filename: qbfmerge.py

import sys, os, string, getopt

## start function usage
def usage():
    helptext = """
Format for command is:

    {} -[hv] [-0 HISTFILE] [-1 VALS -2 TBEND|-p PATH]

Options:
    -h --help
            Show this help text.

    -v --verbose
            Show more information when running the script.

    -0 HISTFILE, --hist=HISTFILE
            History file, defaults to "History.exh" in the current directory.

    -1 VALS, --vals=VALS
            Vals file, eg Cvals.dat, Cppvals.dat

    -2 TBEND, --tbend=TBEND
            TBend file, eg Ctbend.dat, Cpptbend.dat

    -p PATH, --path=PATH
            Path to LDRA installation directory containing data files.

Usage:
    - Merges information from a History.exh file into <lang>vals.dat and
      <lang>tbend.dat files.
    - Exactly one history file must be given.
    - At least one <lang>vals.dat and one <lang>tbend.dat files must be given.
    - Each additional file will be processed in the same way as the first,
      useful for generating Cvals.dat and Cppvals.dat.
    - A path to the location of the data files can be provided instead of, or
      in addition to, the individual files.
        - This path should be a path to the LDRA installation directory. This
          will cause the C and CPP files found there to be merged.
""".format(sys.argv[0])
    print(helptext)
## end function usage

## start function verbose
def verbose(msg):
    global verb
    if verb:
        print(msg)
## end function verbose

## start function readHistory
def readHistory(histfile):
    sec = 0
    vals = []
    tbend = []
    global cpu
    cpu = ''

    with open(histfile, 'rb') as fox:
        verbose('Opening file: ' + fox.name)

        # For every line in the file, assign a "section", 0 is other, 1 is vals
        # and 2 is tbend. Then for each line within the section add it to the
        # correct array. Sections are delimited by the headings and empty
        # lines, underlines are ignored.
        for line in fox:

            # Get value of cpu variable
            linenospace = line.decode("utf8").rstrip().replace(' ', '')
            if linenospace.startswith('CPU='):
                cpu = linenospace.replace('CPU=',  '')
                verbose('Found CPU: ' + cpu)
                continue

            # Determine sections
            if line.startswith(b'<lang>vals.dat'):
                sec = 1
                verbose('Found vals section')
                continue
            if line.startswith(b'<lang>tbend.dat'):
                sec = 2
                verbose('Found tbend section')
                continue
            if line.startswith(b'Quick Brown Fox Test'):
                break

            # Length check is for empty lines that just contain \n or \r\n,
            # also check for underlines to other sections.
            if len(line) < 3 or b'======' in line:
                continue

            if sec == 1:
                vals.append(line)
            elif sec == 2:
                tbend.append(line)

    # If there was no value in the file for the CPU, the var will be empty,
    # give it a default value, otherwise, remove chars that can't be used in
    # filenames.
    if not cpu:
        cpu = 'new'
    else:
        cpu = str(cpu).translate(string.maketrans("",""), string.punctuation)
        cpu = cpu.replace(' ', '_')

    return HistoryObject(vals, tbend)
## end function readHistory

## start class HistoryObject
class HistoryObject(object):
    vals = []
    tbend = []

    def __init__(self, vals, tbend):
        self.vals = vals
        self.tbend = tbend
## end class HistoryObject

## start function mergevals
def mergevals(cpyvals, valsfile):
    valbase = os.path.basename(valsfile)
    newvals = open(cpu + '_' + valbase, 'wb')
    with open(valsfile, 'rb') as origvals:
        verbose('Opening file: ' + origvals.name)
        for line in origvals:
            for entry in cpyvals:

                # Match lines based on code number at start (3 digits + space)
                if line.startswith(entry[:3] + b' '):
                    line = entry
                    cpyvals.remove(entry)
                    break

            newvals.write(line)
    newvals.close()
    verbose("Written file: " + newvals.name)

    if len(cpyvals) > 0:
        exstatus += 1
        for a in cpyvals:
            verbose(a)
## end function mergevals

## start function mergetbend
def mergetbend(cpybend, bendfile):
    bendbase = os.path.basename(bendfile)
    newbend = open(cpu + '_' + bendbase, 'wb')
    with open(bendfile, 'rb') as origbend:
        verbose('Opening file: ' + origbend.name)
        for line in origbend:
            for entry in cpybend:

                # Extract variable type from line (follows the text 'width of')
                # and use this to match against lines from history.exh.
                entrystr = entry.decode('utf8')
                linestr = line.decode("utf8")
                ctype = entrystr[entrystr.index('width of'):]
                if ctype in linestr:
                    line = entry
                    cpybend.remove(entry)
                    break

            newbend.write(line)
    newbend.close()
    verbose("Written file: " + newbend.name)

    if len(cpybend) > 0:
        exstatus += 2
        for a in cpybend:
            verbose(a)
## end function mergetbend

cpu = ''
valsfiles = []
bendfiles = []
exstatus = 0
verb = False

# Check input parameters
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hv0:1:2:p:', ['help', 'verbose', 'hist=', 'vals=', 'tbend=', 'path='])
    except getopt.GetoptError as opterr:
        print(str(opterr))
        usage()
        sys.exit(1)

    if len(opts) == 0:
        usage()
        sys.exit(1)

    global verb
    global valsfiles
    global bendfiles
    histfile = 'History.exh'
    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            verb = True
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-p', '--path'):
            arg = arg.rstrip('/\\')
            valsfiles.append(arg + os.sep + 'C' + os.sep + 'Cvals.dat')
            valsfiles.append(arg + os.sep + 'Cpp' + os.sep + 'Cppvals.dat')
            bendfiles.append(arg + os.sep + 'C' + os.sep + 'Ctbend.dat')
            bendfiles.append(arg + os.sep + 'Cpp' + os.sep + 'Cpptbend.dat')
        elif opt in ('-0', '--hist'):
            histfile = arg
        elif opt in ('-1', '--vals'):
            valsfiles.append(arg)
        elif opt in ('-2', '--tbend'):
            bendfiles.append(arg)
        else:
            assert False, "unknown option"

    # Report and check all files can be read succesfully
    verbose('------------------------')
    verbose('History file: ' + histfile)
    for i in valsfiles:
        verbose('Vals file: ' + i)
    for i in bendfiles:
        verbose('TBend file: ' + i)
    verbose('------------------------')

    for i in [histfile] + valsfiles + bendfiles:
        if not os.access(i, os.R_OK):
            print('Cannot read file ' + i)
            sys.exit(13)

    if not histfile.endswith('.exh'):
        print('History file is not in the correct format.')
        sys.exit(10)
    for f in valsfiles + bendfiles:
        if not f.endswith('.dat'):
            print('Data file is not in the correct format.')
            sys.exit(11)

    history = readHistory(histfile)

    # Parse and merge Cvals.dat file
    for valsfile in valsfiles:
        mergevals(history.vals, valsfile)

    # Parse and merge Ctbend.dat file
    for bendfile in bendfiles:
        mergetbend(history.tbend, bendfile)

    # If there were any lines from the history file that were not merged into
    # the data file, print them and set the exit status accordingly.
    verbose("Finished with exit status: " + str(exstatus))
    sys.exit(exstatus)

if __name__ == "__main__":
    main(sys.argv[1:])
