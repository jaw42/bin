#!/bin/bash

Dir="Pictures/Wallpapers/Active/"

#if [ ! -d "$Dir" ]; then
#    echo "Not Exist $Dir"
#    exit 1
#fi

SetBG () {
  TotalFiles=$( ls -1 "$Dir" | wc -l )
  RandomNumber1=$(( $RANDOM % $TotalFiles ))
  RandomNumber2=$(( $RANDOM % $TotalFiles ))
  test ! $RandomNumber = 0 || RandomNumber=1

  RandomFile1="$( ls -1 $Dir | head -n $RandomNumber1 | tail -n 1)"
  RandomFile2="$( ls -1 $Dir | head -n $RandomNumber2 | tail -n 1)"

  echo "Selected File1: $RandomNumber1: $RandomFile1"
  echo "Selected File2: $RandomNumber2: $RandomFile2"
  #feh --bg-fill "${Dir%/}/${RandomFile1}"
  imlibsetroot -x 1 -s f "${Dir%/}/${RandomFile1}" -x 0 -s f "${Dir%/}/${RandomFile2}"
}

while true; do
    SetBG
    sleep 10m
done


#imlibsetroot -x 1 -s f Pictures/Wallpapers/Active/16.jpg -x 0 -s f Pictures/Wallpapers/Active/159.jpg
