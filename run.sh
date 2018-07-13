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
    RESULT=`find /var/run/screen -name "*.osfw-sensor"`
    if [ -z "$RESULT" ]; then
	screen -dmS osfw-sensor python osfw.py daemon/sensor
    fi
    RESULT=`find /var/run/screen -name "*.osfw-syncfw"`
    if [ -z "$RESULT" ]; then
	screen -dmS osfw-syncfw python osfw.py daemon/syncfw
    fi
    RESULT=`find /var/run/screen -name "*.osfw-webapp"`
    if [ -z "$RESULT" ]; then
	screen -dmS osfw-webapp python osfw.py webapp
    fi
else
    python osfw.py "$1"
fi

popd > /dev/null 2>&1
