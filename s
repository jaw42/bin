#!/bin/bash
# Created:  Thu 07 Aug 2014
# Modified: Tue 17 Feb 2015
# Author:   Josh Wainwright
# Filename: s (Search for files and text)
set -o nounset
set -o errexit
function echoerr() {
	>&2 echo $@
}

cmd=""
verbose=false
dryrun=false
i=""
s=""
r=""
v=""
f=""
o=""
allow_locate=false
allow_git=true
allow_parallel=false
allow_pt=false
allow_ag=true
allow_ack=true

usage() {
	b="\033[4m" # Bold text
	n="\033[0m" # Normal text
helptext="$(basename $0) [-disrvflVh] [PATTERN|FILE]

Search, using the best tools availible, for text or files.

Options:
	-d  ${b}d${n}ryrun, don't search, just show the command that would be run
	-i  case-${b}i${n}nsensitive search*
	-s  ${b}s${n}mart-case search*
	-r  ${b}r${n}egular-expression based search*
	-v  in${b}v${n}ert matches*
	-f  ${b}f${n}ilename search
	-l  allow ${b}l${n}ocate to be used
	-L  don't allow ${b}L${n}ocate to be used
	-G  don't allow ${b}G${n}it to be used
	-p  use ${b}p${n}arallel to search within multiple directories
	    simultaneously. Currently only uses git to search so git must be
	    installed.*
	-P  don't allow ${b}P${n}arallel to be used
	-o  pass extra ${b}o${n}ptions to the selected search tool
	-V  ${b}V${n}erbose output
	-h  show this ${b}h${n}elp text

(*options subject to the feature being availible in the underlying command.)

Search Methods:
	File Search
	-----------
	locate FILE
	git ls-files | grep FILE
	ag -g FILE
	pt -g FILE
	find . | grep FILE

	String Search
	-------------
	git grep STRING
	ag STRING
	pt STRING
	ack STRING
	grep -R STRING"
echo -e "$helptext"
}

verbose() {
	set +u
	if $verbose; then
		echo -e ${2} "$1"
	fi
	set -u
}

useloc() {
	cmd="locate $i $r \"$@\" | grep \"$PWD\" | sed 's#'"$PWD"'/##'"
}


usegit() {
	if [[ "x$r" != "x" ]]; then
		r="-E"
	fi

	if [[ $f = "files" ]]; then
		cmd="git ls-files | \grep $o $i $v $r \"$@\""
	else
		cmd="git grep $o $i $v $r \"$@\""
	fi
}
useag() {
	local ag_files=""
	if [[ $f = "files" ]]; then
		ag_files="-g"
	fi
	cmd="ag --nogroup --hidden $o $i $s $v $ag_files \"$@\" ."
}
usept() {
	local pt_files=""
	if [[ $f = "files" ]]; then
		pt_files="-g"
	fi
	if [ ! -z $v ]; then 
		allow_pt=false
		search_tool "$@"
	else
		cmd="pt --color --nogroup $o $i $s $pt_files \"$@\" ."
	fi
}
useack() {
	if [[ "x$r" != "x" ]]; then
		r="-E"
	fi

	if [[ $f = "files" ]]; then
		cmd="find . | grep $o $i $v $r \"$@\""
	else
		cmd="ack $o $i $s $v \"$@\""
	fi
}
usegrep() {
	if [[ "x$r" != "x" ]]; then
		r="-E"
	fi

	if [[ $f = "files" ]]; then
		cmd="find . | grep $o $i $v $r \"$@\""
	else
		cmd="grep $r -n --recursive $o $i $v \"$@\""
	fi
}
useparallel() {
	if $allow_locate; then
		local find_cmd="dirname \$(locate -br '\.git$')"
	else
		local find_cmd="find ~/ -name \".git\" -exec dirname {} \; 2> /dev/null"
	fi
	cmd="$find_cmd | parallel \"cd {}; git grep --color=always -I $i '$@'\" 2> /dev/null"
}

checkgit() {
	git rev-parse --git-dir > /dev/null 2>&1
	return $?
}

checksvn() {
	svn info > /dev/null 2>&1
	return $?
}

search_tool() {
	if $allow_git && checkgit; then
		usegit "$@"

	elif $allow_parallel; then
		useparallel "$@"

	elif $allow_locate && [ "$f" == "files" ] && hash locate 2> /dev/null; then
		useloc "$@"

	elif $allow_pt && hash pt 2> /dev/null; then
		usept "$@"

	elif $allow_ag && hash ag 2> /dev/null; then
		useag "$@"

	elif $allow_ack && hash ack 2> /dev/null; then
		useack "$@"

	else
		usegrep "$@"
	fi
}

while getopts "disrvflLGpPo:Vh" opt; do
	case "$opt" in
		d) dryrun=true ;;
		i) i="--ignore-case" ;;
		s) s="--smart-case" ;;
		r) r="--regex" ;;
		v) v="--invert-match" ;;
		f) f="files" ;;
		l) hash locate 2>&1 > /dev/null && allow_locate=true ;;
		L) allow_locate=false ;;
		p) hash parallel 2>&1 > /dev/null && allow_parallel=true ;;
		P) allow_parallel=false ;;
		G) allow_git=false ;;
		o) o="$OPTARG" ;;
		V) verbose=true ;;
		h) usage && exit 0 ;;
		*) echoerr "Flag "$opt" not recognised."
			exit 1
			;;
	esac
done
shift $((OPTIND-1))

if checksvn; then
	allow_git=false
fi

search_tool "$@"

if $dryrun; then

	verbose "verbose       : $verbose"
	verbose "dryrun        : $dryrun"
	verbose "ignore case i : $i"
	verbose "smart case  s : $s"
	verbose "regex       r : $r"
	verbose "invert      v : $v"
	verbose "file search f : $f"
	verbose "allow_locate  : $allow_locate"
	verbose "allow_git     : $allow_git"
	verbose "allow_parallel: $allow_parallel"

	echo "**** Dry Run ****"
	echo "$cmd"
else
	verbose "##"
	verbose "# $cmd"
	verbose "##"
	eval "$cmd"
fi
