#!/bin/bash
# Created:  Tue 14 Apr 2015
# Modified: Wed 15 Apr 2015
# Author:   Josh Wainwright
# Filename: dlbooks.sh

cnt=0
while read a; do
	book=${a% *}
	tot=${a#* }
	cnt=$((cnt+1))
	cnt0=$(printf "%02d" $cnt)
	for i in `seq 1 $tot`; do
		i0=$(printf "%02d" $i)
		printf "${book}: ${i0}/${tot}\n"
		curl -s http://biblehub.com/esv/${book}/${i}.htm > ${cnt0}_${book}_${i0}.txt
	done
done < ../books
