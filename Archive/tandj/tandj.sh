#!/bin/bash
set -o nounset
set -o errexit

video_player="/cygdrive/c/progs/mpv-x86_64-latest/mpv.exe"
mpv=mpv

if ! hash mpv 2> /dev/null; then
	mpv=mplayer
	if ! hash mplayer 2> /dev/null; then
		mpv="$video_player"
	fi
fi
ff=mp4
i=0
if [[ $# -eq 0 ]]; then
	startnum=$(($(tail -n1 "$0" | sed -r 's/# Latest: << (.*) >>/\1/')+1))
else
	startnum=$1
fi
list=$(grep $ff tandj.html | sed -r 's/^<a href="(.*)".*$/\1/' | sed "s/$ff.*/$ff/")
for link in $list; do
	i=$((i+1))
	if [[ $i -lt $startnum ]]; then
		continue
	fi
	printf -v j "%03d" $i
	echo $j
	name=tandj$j.$ff.download
	if [ ! -f $name ]; then
		{
			echo $name
			remote_size=$(curl -sI "$link" | awk '/Content-Length/ {print $2'})
			echo "remote size = $remote_size"
			r_s_red=$((remote_size/12))
			sleep 5s
			while [[ $(stat -c "%s" $name 2> /dev/null) -lt $r_s_red ]]; do
				echo -en "\b\b\b\b\b      small"
				sleep 5s
			done
			eval $mpv --really-quiet $name
		} &
		pid=$!
		trap "kill $pid; rm *.download; exit 1" SIGINT SIGTERM
		curl --location -o "$name" "$link"
	else
		# The file already exists, so play it.
		eval $mpv --really-quiet $name
	fi
	while ! mv $name ${name%.download} 2> /dev/null; do
		sleep 1s
	done
	sed -ri "s/^(# Latest: <<).*(>>)/\1 $i \2/" "$0"
	break
done

# Latest: << 39 >>
