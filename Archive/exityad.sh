#!/bin/bash

title="Actions"
action=$(yad --width 300 --entry --title="$title" --undecorated --borders=10 --window-icon=gtk-quit\
    --image=gtk-quit \
    --button="gtk-close:1" --button="gtk-ok:0" \
    --text "Choose action:" \
    --entry-text \
    "Suspend" "Shutdown" "Logout" "Restart")
    
ret=$?

[[ $ret -eq 1 ]] && exit 0

case $action in
    Logout*) cmd="openbox --exit" ;;
    Suspend*) cmd="sudo pm-suspend" ;;
    Shutdown*) cmd="sudo shutdown -h now" ;;
    Restart*) cmd="sudo shutdown -r now" ;;
    *) exit 1 ;;        
esac

eval exec $cmd
