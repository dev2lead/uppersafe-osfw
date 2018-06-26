#!/bin/bash
##
# Nicolas THIBAUT
# nicolas.thibaut@l-3s.com
##

pushd `dirname "$0"` > /dev/null 2>&1

source venv/bin/activate

shopt -s expand_aliases

export PYTHONDONTWRITEBYTECODE="1"
export LC_ALL="C.UTF-8"
export LANG="C.UTF-8"

if [ -z "$1" ]; then
    screen -h 1000000 -dmS osfw-sensor bash run.sh daemon/sensor
    screen -h 1000000 -dmS osfw-syncfw bash run.sh daemon/syncfw
    screen -h 1000000 -dmS osfw-webapp bash run.sh webapp
fi

if [ "$1" == "daemon/sensor" ]; then
    python main.py daemon/sensor
fi

if [ "$1" == "daemon/syncfw" ]; then
    python main.py daemon/syncfw
fi

if [ "$1" == "webapp" ]; then
    python main.py webapp | tee assets/logs.txt
fi

popd > /dev/null 2>&1
