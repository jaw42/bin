	#!/bin/bash

title="EXIT: What do you want to do ?"
exit_type=`zenity  --width="530" --height="275" --title="$title" --list --radiolist --column="Click Here" \
	--column="Exit Type" --column="Description" \
	TRUE "Logout" "Log Current User out and return to Login Screen"\
	FALSE "Suspend" "Put the computer to sleep"\
	FALSE "Resart" "Resart the PC"\
	FALSE "Shutdown" "Shutdown the PC"\
	FALSE "Cancel" "Cancel the Exit" \
	FALSE "Monitor" "Turn off the computer screen"\
	| sed 's/ max//g' `

echo "$exit_type chosen to Exit."

if [ "$exit_type" = "Logout" ]
then 
		#for i in $(seq 0 100) 
		#do echo $i;
		#sleep 0.005;
		#done | yad --progress --image=gtk-orientation-portrait --window-icon=gtk-dialog-info --text="Logging Out..." --auto-close --auto-kill --title=Logout --width=300 | notify-send -i gtk-orientation-portrait Logout && openbox --exit
		openbox --exit

elif [ "$exit_type" = "Suspend" ]
then
		for i in $(seq 0 100) 
		do echo $i;
		sleep 0.005;
		done | yad --progress --image=gtk-close --window-icon=gtk-dialog-info --text="Suspending..." --auto-close --auto-kill --title=Logout --width=300 | notify-send -i gtk-close Suspend && sudo pm-suspend

elif [ "$exit_type" = "Resart" ]
then
        for i in $(seq 0 100) 
		do echo $i;
		sleep 0.005;
		done | yad --progress --image=gtk-refresh --window-icon=gtk-dialog-info --text="Restarting..." --auto-close --auto-kill --title=Logout --width=300 | notify-send -i gtk-refresh Restart && sudo shutdown -r now


elif [ "$exit_type" = "Shutdown" ]
then
        for i in $(seq 0 100) 
		do echo $i;
		sleep 0.005;
		done | yad --progress --image=gtk-quit --window-icon=gtk-dialog-info --text="shutting down..." --auto-close --auto-kill --title=Logout --width=300 | notify-send -i gtk-quit Shutdown && sudo shutdown -h now


elif [ "$exit_type" = "Monitor" ]
then
       xset dpms force off
else

#if [ "$exit_type" = "Cancel" ]
#then
		notify-send -i gtk-dialog-info Canceled 
fi
