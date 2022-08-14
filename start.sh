#!/bin/bash

mkdir -p ./logs


user=`echo $USER`
if [ "$user" != "root" ]; then
  echo "Script must be run as root.  Try 'sudo ./start.sh'"
  exit 1
fi

to_start=(
  "battery"
  "central_hub"
  "compass"
  "depth"
  "motor_control"
  "onboard_ui"
  "system_stats"
  "vision"
)

if [ $# -ne 0 ]; then
  to_start=($@)
fi

for sub_system in ${to_start[@]}
do
  echo "starting $sub_system"
  python3 src/start_$sub_system.py > ./logs/$sub_system.log 2>&1 &
  echo $! > ./$sub_system.pid
done

