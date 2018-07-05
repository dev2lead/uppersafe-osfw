#!/bin/bash
##
# Nicolas THIBAUT
# nicolas.thibaut@uppersafe.com
##

### BEGIN INIT INFO
# Provides:		osfw
# Required-Start:	$local_fs $network $remote_fs $syslog
# Required-Stop:	$local_fs $network $remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	OSFW
# Description:		UPPERSAFE-OSFW
### END INIT INFO

export PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

SUCCESS=2
FAILURE=0

if [ "$1" == "start" ]; then
    sleep 30

    bash /root/osfw/run.sh

    systemctl restart unbound

    exit "$SUCCESS"
else
    exit "$FAILURE"
fi
