#!/bin/bash

hour=$(date +%-H)
day=$(date +%j)

if [[ $hour -ge 5 && $hour -lt 10 ]]; then
    echo -n "Dawn"
    state=dawn
    number=1
elif [[ $hour -ge 10 && $hour -lt 16 ]]; then
    echo -n "Day"
    state=day
    number=2
elif [[ $hour -ge 16 && $hour -lt 20 ]]; then
    echo -n "Dusk"
    state=dusk
    number=3
else
    echo -n "Its now night"
    state=night
    number=4
fi

if [[ $day%3 -eq 0 ]]; then
    number=$(($number + 4))
elif [[ $day%3 -eq 1 ]]; then
    number=$(($number + 8))
fi
echo " Number=$number"

imlibsetroot -x 1 -s f ~/Pictures/Wallpapers/Google\ Now/$number.jpg -x 0 -s f  ~/Pictures/Wallpapers/Google\ Now/$number.jpg 
