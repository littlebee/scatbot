#!/bin/bash

# don't stop on error - let other subs exit if any sub fails to exit
# set -e

# user=`echo $USER`
# if [ "$user" != "root" ]; then
#   echo "Script must be run as root.  Try 'sudo ./stop.sh'"
#   exit 1
# fi

to_stop=()
if [ $# -ne 0 ]; then
  to_stop=($@)
else
  IFS=$'\n' read -d '' -r -a to_stop < ./services.cfg
fi

// stop in reverse order as start
for ((i=${#to_stop[@]}-1; i>=0; i--));
do
  sub_system=${to_stop[i]}
  echo "stopping $sub_system"

  pid_file="./$sub_system.pid"
  if [[ "$sub_system" == *".pid" ]]; then
    pid_file="./$sub_system"
  fi

  if [ -f "$pid_file" ]; then
    kill -1 `cat $pid_file`
    rm -f $pid_file
  else
    echo "$pid_file does not exist. skipping"
  fi
done
