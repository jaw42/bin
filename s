#!/bin/bash
set -o nounset
set -o errexit

cmd=""
verbose=false
dryrun=false
i=""
s=""
r=""
v=""
f=""
allow_locate=false
allow_git=true
allow_parallel=false

usage() {
	b="\033[4m" # Bold text
	n="\033[0m" # Normal text
helptext="$(basename $0) [-disrvflVh] [PATTERN|FILE]

s - ${b}S${n}earch, using the best tools availible, for text or files.

Options:
	-d  ${b}d${n}ryrun, don't do anything, just show the command that would be run
	-i  case-${b}i${n}nsensitive search*
	-s  ${b}s${n}mart-case search*
	-r  ${b}r${n}egular-expression based search*
	-v  in${b}v${n}ert matches*
	-f  ${b}f${n}ilename search
	-l  allow ${b}l${n}ocate to be used
	-V  ${b}V${n}erbose output
	-h  show this ${b}h${n}elp text

	(*options are subject to the feature being availible in the underlying command.)

Search Methods:
	File Search
	-----------
	locate FILE
	git ls-files | grep FILE
	ag -g FILE
	find . | grep FILE

	String Search
	-------------
	git grep STRING
	ag STRING
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
		cmd="git ls-files | \grep $i $v $r \"$@\""
	else
		cmd="git grep $i $v $r \"$@\""
	fi
}
useag() {
	if [[ $f = "files" ]]; then
		cmd="ag --hidden $i $s $v -g \"$@\" ."
	else
		cmd="ag --hidden $i $s $v \"$@\" ."
	fi
}
useack() {
	if [[ "x$r" != "x" ]]; then
		r="-E"
	fi

	if [[ $f = "files" ]]; then
		cmd="find . | grep $i $v $r \"$@\""
	else
		cmd="ack $i $s $v \"$@\""
	fi
}
usegrep() {
	if [[ "x$r" != "x" ]]; then
		r="-E"
	fi

	if [[ $f = "files" ]]; then
		cmd="find . | grep $i $v $r \"$@\""
	else
		cmd="grep $r -n --recursive $i $v \"$@\""
	fi
}
useparallel() {
	hash parallel 2>&1 >/dev/null || exit 1
	local par_cmd="cd {}/..; git grep --color=always -I $i \"$@\""
	if $allow_locate && $allow_git; then
		local find_cmd="locate --regex \"$(pwd).*.git$\""
	elif $allow_git;then
		local find_cmd="find -name \"*.git\""
	fi
	exec $find_cmd | parallel $par_cmd
	echo status $?
}

checkgit() {
	git rev-parse --git-dir > /dev/null 2>&1
	return $?
}

checksvn() {
	svn info > /dev/null 2>&1
	return $?
}

while getopts "disrvflpVh" opt; do
	case "$opt" in
		d)
			dryrun=true
			;;
		i)
			i="--ignore-case"
			;;
		s)
			s="--smart-case"
			;;
		r)
			r="--regex"
			;;
		v)
			v="--invert-match"
			;;
		f)
			f="files"
			;;
		l)
			allow_locate=true
			;;
		p)
			allow_parallel=true
			;;
		V)
			verbose=true
			;;
		h)
			usage
			exit 0
			;;
		*)
			echo "Flag "$opt" not recognised."
			exit 1
			;;
	esac
done
shift $((OPTIND-1))

if checksvn; then
	allow_git=false
fi

if $allow_git && \
	checkgit; then
	usegit "$@"

elif $allow_parallel; then
	useparallel "$@"

elif [ "$f" == "files" ] && \
	$allow_locate && \
	hash locate 2> /dev/null; then
	useloc "$@"

elif hash ag 2> /dev/null; then
	useag "$@"

elif hash ack 2> /dev/null; then
	useack "$@"

else
	usegrep "$@"
fi

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
	verbose "$cmd"
	eval "$cmd"
fi
