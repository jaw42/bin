#!/bin/bash
# Created:  Wed 18 Mar 2015
# Modified: Thu 19 Mar 2015
# Author:   Josh Wainwright
# Filename: ts_to_unix.sh

set -o nounset

convertsecs() {
	((h=${1}/3600))
	((m=(${1}%3600)/60))
	((s=${1}%60))
	printf "%02d:%02d:%02d\n" $h $m $s
}

countlines() {
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

str2ts() {
	h=${1:0:2}
	((h=${h#0}*60*60))
	m=${1:2:2}
	((m=${m#0}*60))
	s=${1:4:2}
	((s=${s#0}))
	((ts=$h+$m+$s))
	printf "$ts"
}

loop() {
	f=$1
	total=0
	while read str; do
		ts=$(str2ts $str)
		total=$((total + ts))
	done < <(head -n "$length" <<< "$file" | cut -d, -f "$f")
	echo "$total"
}

file=$(grep -vE "^#|^$" times.txt)
length=$(countlines -v "$file")
length=$((length - 1))

total=$(loop 2)
av_arrive=$((total / length))
av_arrive2=$(convertsecs $((total / length)) )
printf "%-15s %8s\n" "Arrive" "$av_arrive2"

total=$(loop 5)
av_leave=$((total / length))
av_leave2=$(convertsecs $((total / length)) )
printf "%-15s %8s\n" "Leave" "$av_leave2"

total=$(loop 3)
av_lstart=$((total / length))
av_lstart2=$(convertsecs $((total / length)) )
printf "%-15s %8s\n" "Lunch Start" "$av_lstart2"

total=$(loop 4)
av_lend=$((total / length))
av_lend2=$(convertsecs $((total / length)) )
printf "%-15s %8s\n" "Lunch End" "$av_lend2"

av_day=$(convertsecs $((av_leave - av_arrive)) )
av_day=${av_day#0}
printf "%-15s %8s\n" "Working Day" "$av_day"

av_lunch=$(convertsecs $((av_lend - av_lstart)) )
av_lunch=${av_lunch#00:}
printf "%-15s %8s\n" "Lunch Break" "$av_lunch"
