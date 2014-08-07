 #!/bin/bash
set -o nounset
set -o errexit

verbose=false
i=""
s=""
v=""

verbose() {
	set +u
	if $verbose; then
		echo -e ${2} "$1"
	fi
	set -u
}

usegit() {
	verbose "git"
	git grep $i $v "$@"
}
useag() {
	verbose "ag"
	ag $i $s $v "$@"
}
useack() {
	verbose "ack"
	ack $i $s $v "$@"
}
usegrep() {
	verbose "grep"
	grep --recursive $i $v "$@"
}

while getopts "isvV" opt; do
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
