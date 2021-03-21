#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
  echo "Quiting ADD Video"
  kill -9 `cat button_activator_pid.txt`
  rm button_activator_pid.txt
}

source ./venv/bin/activate
nohup button_activator.py > button_activator.log 2>&1 &
echo $! > button_activator_pid.txt
python app.py
