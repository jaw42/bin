#!/bin/bash
logfile="/home/josh/Bin/duck.log"
echo url="https://www.duckdns.org/update?domains=joshaw&token=e721456d-0a62-4fa9-992a-754c797ae1b8&ip=" | curl -s -k -o $logfile -K -
cat $logfile
