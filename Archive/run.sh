#! /bin/bash

XTERM="xterm"

# create history file
mkdir -p ${XDG_CACHE_HOME:-$HOME/.cache}/
HISTFILE=${XDG_CACHE_HOME:-$HOME/.cache}/ix-run.history
touch $HISTFILE

# create and run dialog
TITLE="Run command"
TEXT="\nEnter command to execute:\n"
CMD='yad --width=500 --center --window-icon="gtk-execute" --name="${0##*/}" --title="$TITLE" --text="$TEXT" --image="gtk-execute" --entry --editable'
ARGS=$(perl -pe 's/(^.*$)/"\1"/;s/\n/ /' $HISTFILE)
rcmd=$(eval $CMD $ARGS)

[[ -z "$rcmd" ]] && exit 0

# run command
case $rcmd in
    www*|http://*|https://*|ftp://*|www*)
        xdg-open $rcmd &
        ;;
    mailto://*)
        xdg-email $rcmd &
        ;;
    man://*)
        eval $XTERM -e "man ${rcmd#man://}" &
        ;;
    telnet*|ssh*)
        eval $XTERM -e "$rcmd" &
        ;;
    *)
        eval $rcmd &
        ;;
esac

# add command to history
grep -q -F "$rcmd" $HISTFILE || echo $rcmd >> $HISTFILE

exit 0
