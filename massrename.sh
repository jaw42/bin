#!/bin/sh
# Created:  Tue 07 Nov 2017
# Modified: Thu 09 Nov 2017
# Author:   Josh Wainwright
# Filename: massrename.sh
if [ "$1" = "-h" ]; then
	cat <<EOF
Rename files and folders using $EDITOR (\$EDITOR)

$ massrename.sh PATH
	Selects all files in specified PATH

$ find -type f | massrename.sh
	Selects all newline separated files or folders passed to stdin
EOF
	exit
fi

if [ $# -gt 0 ]; then
	path=${1}
	list=$(find "$path" -maxdepth 1 -type f)
else
	list=$(cat)
	printf 'Reading from STDIN\n' 1>&2 
fi

tmpf=$(mktemp)
printf "$list\n" > "$tmpf.orig"
printf "$list\n" > "$tmpf"

count_before=$(wc -l < "$tmpf.orig")
printf '%i files selected\n' "$count_before" 1>&2

$EDITOR "$tmpf"

if [ "$count_before" -ne "$(wc -l < "$tmpf")" ]; then
	echo "Don't add or remove lines"
	exit
fi

if cmp -s "$tmpf.orig" "$tmpf"; then
	echo "No changes made."
	exit
fi

IFS='\t' paste "$tmpf.orig" "$tmpf" | while read before after; do
	if [ "$before" != "$after" ]; then
		echo "$before -> $after"
		mv "$before" "$after"
	fi
done

rm -f "$tmpf.orig" "$tmpf"
