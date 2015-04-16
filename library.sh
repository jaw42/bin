# Created:  Thu 16 Apr 2015
# Modified: Thu 16 Apr 2015
# Author:   Josh Wainwright
# Filename: library.sh
set -o nounset
set -o errexit

echoerr() {
	>&2 echo $@
}

exists() {
	command -v "$@" > /dev/null
}

usage() {
	helptext="$(basename $0) []"
	printf "$helptext"
}

countlines() {
	# if the -v flag is given, then count the lines from the given variable,
	# otherwise, the lines from the result of running the command.
	if [ "$1" == "-v" ]; then
		shift
		local out="$@"
	else
		local out=$(eval $@)
	fi
	local newl=${out//[^$'\n']}
	local numl=${#newl}
	if ! [ -z "$out" ]; then
		numl=$((numl + 1))
	fi
	printf $numl
}

