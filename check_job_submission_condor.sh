#!/bin/sh

# Returns success if condor_submit returns 0 exit code, otherwise returns error

TMPDIR="/tmp"
HOME="/tmp"
CONDOR_SUBMIT="/usr/bin/condor_submit" 
CMDS="executable = /bin/sleep\narguments = 1\nrequest_memory=0\nNotification = Never\naccounting_group = group_OTHER.nagios\nQueue"
cd ${TMPDIR}
printf "${CMDS}" | ${CONDOR_SUBMIT} 2>&1

if [ $? != 0 ]; then
        exit 2
fi

exit 0


