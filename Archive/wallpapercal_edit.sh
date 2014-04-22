#! /bin/zsh

##Original wallpaper image that will be kept clean
#ORIG=/home/josh/Pictures/Wallpapers/Luna/Leaves.jpg
ORIG=$(grep -E -o '/home.*jpg' .fehbg)

##New wallpaper that will have cal written to and will be overwritten
NEW=/home/josh/Pictures/Wallpapers/Luna/Leaves_cal.jpg

##Cal command with day highlight. Change [,] to have different day highlight
CAL=$(echo `date "+%d %B %Y"` | awk '{ print substr("          ",1,(21-length($0))/2) $0; }'; cal -s | awk '{ getline; print " Mo Tu We Th Fr Sa Su"; getline; if (substr($0,1,2) == " 1")  print "                    1 "; do { prevline=$0; if (getline == 0) exit; print " " substr(prevline,4,17) " " substr($0,1,2) " "; } while (1) }' | awk -v cday=`date "+%d"` '{ fill=(int(cday)>9?"":" ");    a=$0; sub(" "fill int(cday)" ","["fill int(cday)"]",a); print  a }')

##Write calendar on to defined image
convert $ORIG -pointsize 30 -fill white -font Droid-Sans-Mono-Regular -draw "text 30,1250 ' $CAL'" $NEW

##Append to previous for black line at top for panel
#-draw " fill #262729 rectangle 0,0 900,66" $NEW

#cal -y | awk -v month="`date +%m`" -v day="`date +%e` " '{m=int((NR-3)/8)*3+1; for (i=0;i<3;i++) {t[i]=substr($0,1+i*22,20) " "; if (m+i==month) sub(day,"\033[7m&\033[0m",t[i]);} print t[0],t[1],t[2];}'
