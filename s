 #!/bin/bash
set -o nounset
set -o errexit

verbose=false
i=""
s=""
v=""
f=""

verbose() {
	set +u
	if $verbose; then
		echo -e ${2} "$1"
	fi
	set -u
}

usegit() {
	verbose "git"
	if [[ $f = "files" ]]; then
		git ls-files | \grep $i $v "$@"
	else
		git grep $i $v "$@"
	fi
}
useag() {
	verbose "ag"
	if [[ $f = "files" ]]; then
		ag $i $s $v -g "$@"
	else
		ag $i $s $v "$@"
	fi
}
useack() {
	verbose "ack"
	if [[ $f = "files" ]]; then
		find . | grep $i $v "$@"
	else
		ack $i $s $v "$@"
	fi
}
usegrep() {
	verbose "grep"
	if [[ $f = "files" ]]; then
		find . | grep $i $v "$@"
	else
		grep --recursive $i $v "$@"
	fi
}

while getopts "isvfV" opt; do
	case "$opt" in
		i)
			i="--ignore-case"
			;;
		s)
			s="--smart-case"
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
elif hash ag 2> /dev/null; then
	useag "$@"
elif hash ack 2> /dev/null; then
	useack "$@"
else
	usegrep "$@"
fi

# vim: ft=sh
