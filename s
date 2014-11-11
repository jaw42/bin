#!/bin/bash
set -o nounset
set -o errexit

cmd=""
verbose=false
i=""
s=""
r=""
v=""
f=""

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

while getopts "isrvfV" opt; do
	case "$opt" in
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
		V)
			verbose=true
			;;
		*)
			echo "Flag "$opt" not recognised."
			exit 0
			;;
	esac
done
shift $((OPTIND-1))

if git rev-parse --git-dir > /dev/null 2>&1; then
	usegit "$@"
elif [ "$f" == "files" ] && hash locate 2> /dev/null; then
	useloc "$@"
elif hash ag 2> /dev/null; then
	useag "$@"
elif hash ack 2> /dev/null; then
	useack "$@"
else
	usegrep "$@"
fi

verbose "$cmd"
eval "$cmd"

# vim: ft=sh
