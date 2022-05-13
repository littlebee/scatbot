#!/bin/bash

user=`echo $USER`
if [ "$user" != "root" ]; then
  echo "Script must be run as root.  Try 'sudo ./stop.sh'"
  exit 1
fi

to_stop=(
  "central_hub"
  "compass"
  "motor_control"
  "onboard_ui"
  "system_stats"
  "vision"
)
if [ $# -ne 0 ]; then
  to_stop=($@)
fi

for sub_system in ${to_stop[@]}
do
  echo "stopping $sub_system"
  pid_file="./$sub_system.pid"
  if [ -f "$pid_file" ]; then
    kill -9 `cat $pid_file`
    # rm -f $pid_file
  else
    echo "$pid_file does not exist. skipping"
  fi
done

