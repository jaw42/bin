#!/bin/bash

yes | yad --progress \
		--title="Battery Warning" \
		--text="Battery Low. \nPlease connect to power." \
		--window-icon=gtk-dialog-warning \
		--image=gtk-dialog-warning \
		--undecorated \
		--pulsate \
		--progress-text= \
		--button=Action:$HOME/.scripts/exit.sh \
		--button=gtk-close\

