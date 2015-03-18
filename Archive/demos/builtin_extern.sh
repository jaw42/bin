#!/bin/bash
# Created:  Thu 12 Mar 2015
# Modified: Wed 18 Mar 2015
# Author:   Josh Wainwright
# Filename: testingcygwin.sh

set -o nounset
function echoerr() {
	>&2 echo "$@"
}

var="one
two
three
four
five
six"

echo "$var"

time (
for i in {1..1000}; do
	res="${var//[^$'\n']}"
	res=${#res}
	if ! [ -z "$var" ]; then
		res=$((res + 1))
	fi
	printf "%-5s: %s\r" "$i" "${res}"
done
)

time (
for i in {1..1000}; do
	res="$(echo "$var" | wc -l)"
	printf "%-5s: %s\r" "$i" "${res}"
done
)
