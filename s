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
allow_locate=true

usage() {
	echo "File Search"
	echo "-----------"
	echo "locate FILE"
	echo "git ls-files | grep FILE"
	echo "ag -g FILE"
	echo "find . | grep FILE"
	echo
	echo "String Search"
	echo "-------------"
	echo "git grep STRING"
	echo "ag STRING"
	echo "ack STRING"
	echo "grep -R STRING"
}

verbose() {
	set +u
	if $verbose; then
		echo -e ${2} "$1"
	fi
	set -u
}

useloc() {
	cmd="locate $i $r \"$@\""
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
		cmd="ag $i $s $v -g \"$@\" ."
	else
		cmd="ag $i $s $v \"$@\" ."
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

while getopts "disrvflVh" opt; do
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
			allow_locate=false
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

if git rev-parse --git-dir > /dev/null 2>&1; then
	usegit "$@"
elif [ "$f" == "files" ] && $allow_locate && hash locate 2> /dev/null; then
	useloc "$@"
elif hash ag 2> /dev/null; then
	useag "$@"
elif hash ack 2> /dev/null; then
	useack "$@"
else
	usegrep "$@"
fi

if $dryrun; then
	echo "**** Dry Run ****"
	echo "$cmd"
else
	verbose "$cmd"
	eval "$cmd"
fi
