#!/bin/bash
# Created:
# Modified:
# Author:
# Filename:

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
