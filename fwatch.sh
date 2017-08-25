#!/bin/bash

opt=false
for a in $@; do
	if [ "$a" == "--" ]; then
		opt=true
		continue
	fi
	if $opt; then
		cmd="$cmd $a"
	else
		files="$files $a"
	fi
done

if [ -z "$files" ]; then
    echo "Nothing to watch, abort"
    exit
else
    echo "watching: $files"
    echo "command:  $cmd"
fi

previous_checksum=""
while [ 1 ]; do
    checksum=$(cksum $files | cksum)  
    if [ "$checksum" != "$previous_checksum" ]; then
		date
        eval "$cmd"
    fi
    previous_checksum="$checksum"
    sleep 5
done


