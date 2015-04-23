#!/bin/bash
# Created:  Wed 15 Apr 2015
# Modified: Wed 22 Apr 2015
# Author:   Josh Wainwright
# Filename: splitbible.sh

if [ $# -ne 2 ]; then
	echo "Wrong number of arguements."
	echo "$(basename $0) bible dir"
	exit 1
fi

i=0
newfolder="$2"
mkdir -p "$newfolder"
file="$newfolder/bible"
biblefile="${newfolder}.list"
touch "$file"

while IFS=$'\n' read -r line || [ -n "$LINE" ]; do
	line=${line//$'\t'/    }

	if [ "${line:0:3}" == "###" ]; then
		i=$((i+1))
		i0=$(printf "%02d" $i)
		tmp=${line:4}
		file="$newfolder/${i0}_${tmp// /_}.bible"
		rm -f "$file"
		printf "%s\n" "$file" >> "$biblefile"
		echo "$file"
	fi

	printf "%s\n" "$line" >> "$file"
done < "$1"
