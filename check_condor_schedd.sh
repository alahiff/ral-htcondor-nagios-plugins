#!/bin/bash
# Copyright 2014 Science and Technology Facilities Council
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

