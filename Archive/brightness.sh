#!/bin/bash
#

FILE='/sys/class/backlight/intel_backlight/brightness'
MAX=`cat /sys/class/backlight/intel_backlight/max_brightness`
INIT=`cat /sys/class/backlight/intel_backlight/brightness`

if [ -w "$FILE" ]
then
  echo
else
  gksu chmod 777 /sys/class/backlight/intel_backlight/brightness
fi

NEW=`yad --button=gtk-ok --mouse --on-top --undecorated --window-icon=gtk-properties --width=300 --scale --min-value=100000 --step=10000 --max-value=$MAX --value=$INIT --hide-value`

echo $NEW > $FILE
