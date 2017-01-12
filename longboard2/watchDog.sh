#!/bin/bash

while true
do

TEST=$(ps -A | grep -w lbremote.py)
if ! [ -n "$TEST" ] ; then
    /home/pi/lbshutdown.py </dev/null &>/dev/null 
    sleep 2
    /home/pi/lbremote.py </dev/null &>/dev/null &
fi

sleep 2

done
