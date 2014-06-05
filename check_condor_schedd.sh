#!/bin/bash

fhostname=`hostname -f`
shostname=`hostname -s`

rtnMsg=""
rc=0

scheddcount=`/usr/bin/condor_status -direct $fhostname -schedd | grep -c $shostname `


if [ $scheddcount -eq 1 ]; then
 rtnMsg="Schedd is advertised on $shostname" 
elif [ $scheddcount -eq 0 ]; then
 rtnMsg="Schedd is NOT advertised on $shostname"
 rc=2
else
 rtnMsg="Problem running check. Please investigate."
 rc=3
fi

echo $rtnMsg
exit $rc

