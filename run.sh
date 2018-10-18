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
    RESULT=`supervisorctl pid osfw-sensor`
    if [ "$RESULT" == 0 ]; then
	RESULT=`find /var/run/screen -name "*.osfw-sensor" | wc -l | xargs`
	if [ "$RESULT" == 0 ]; then
	    screen -dmS osfw-sensor python osfw.py daemon/sensor
	else
	    echo "Error: osfw-sensor is already running in a screen"
	fi
    else
	echo "Error: osfw-sensor is already running from supervisor"
    fi
    RESULT=`supervisorctl pid osfw-syncfw`
    if [ "$RESULT" == 0 ]; then
	RESULT=`find /var/run/screen -name "*.osfw-syncfw" | wc -l | xargs`
	if [ "$RESULT" == 0 ]; then
	    screen -dmS osfw-syncfw python osfw.py daemon/syncfw
	else
	    echo "Error: osfw-syncfw is already running in a screen"
	fi
    else
	echo "Error: osfw-syncfw is already running from supervisor"
    fi
    RESULT=`supervisorctl pid osfw-webapp`
    if [ "$RESULT" == 0 ]; then
	RESULT=`find /var/run/screen -name "*.osfw-webapp" | wc -l | xargs`
	if [ "$RESULT" == 0 ]; then
	    screen -dmS osfw-webapp python osfw.py webapp
	else
	    echo "Error: osfw-webapp is already running in a screen"
	fi
    else
	echo "Error: osfw-webapp is already running from supervisor"
    fi
else
    python osfw.py "$1"
fi

popd > /dev/null 2>&1
