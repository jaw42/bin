#!/bin/sh
# Created:  Tue 07 Nov 2017
# Modified: Tue 07 Nov 2017
# Author:   Josh Wainwright
# Filename: massrename.sh

path=${1:-.}
list=$(find "$path" -maxdepth 1 -type f)

tmpf=$(mktemp)
printf "$list\n" > "$tmpf.orig"
printf "$list\n" > "$tmpf"

$EDITOR "$tmpf"

if [ "$(wc -l < "$tmpf.orig")" -ne "$(wc -l < "$tmpf")" ]; then
	echo "Don't add or remove lines"
	exit
fi

IFS='\t' paste "$tmpf.orig" "$tmpf" | while read before after; do
	if [ "$before" != "$after" ]; then
		echo "$before -> $after"
		mv "$before" "$after"
	fi
done

rm -f "$tmpf.orig" "$tmpf"
