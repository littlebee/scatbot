#!/bin/bash

mkdir -p ./logs


# user=`echo $USER`
# if [ "$user" != "root" ]; then
#   echo "Script must be run as root.  Try 'sudo ./start.sh'"
#   exit 1
# fi

sleep=2

to_start=()

if [ $# -ne 0 ]; then
  to_start=($@)
  sleep=0
else
  IFS=$'\n' read -d '' -r -a to_start < ./services.cfg
fi

for sub_system in ${to_start[@]}
do
  echo "starting $sub_system"

  logfile="./logs/$sub_system.log"

  if [ -f "$logfile" ]; then
    mv -f "$logfile" "$logfile".1
  fi

  echo "starting $sub_system at $(date)" >> "$logfile"

  python3 src/start_$sub_system.py > $logfile 2>&1 &

  echo $! > ./$sub_system.pid
  if [[ $sleep > 0 ]]; then
    echo "sleeping for $sleep seconds"
    sleep $sleep
  fi
done
