# linux-server-health-monitoring-script/      #
#! /bin/bash
# unset any variable which system may be using

lastsnap=$(ls *pred* | sort -n | tail -1)
echo $lastsnap
#
n=$(date '+%s')
#echo $now
now="predecir"$n
file="$now.txt"
#echo $file
val=$(top -b -n 1)
echo "$val" > "$file"

