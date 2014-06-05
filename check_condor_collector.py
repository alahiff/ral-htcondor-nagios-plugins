#!/usr/bin/python
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

import htcondor
import classad
import socket

# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3 

rtnMsg = ""

try:
  coll = htcondor.Collector(socket.gethostname())
  collectors = coll.query(htcondor.AdTypes.Collector, "true", ["Name"])
  numCollectors = len(collectors)

  if numCollectors >= 1:
   if numCollectors > 1:
    rtnMsg = "OK: %s collectors running. " % numCollectors
    exitState = OK 
   else:
    rtnMsg="Warning: Only 1 collector running. "
    exitState = WARNING
   for collector in collectors:
    rtnMsg += collector['Name'].strip('RAL-LCG2@').replace(".gridpp.rl.ac.uk","") + " "
  else:
   rtnMsg="Critical: No collectors running."
   exitState = CRITICAL
except Exception,e:
  rtnMsg = "UNKNOWN: Problem running check. " + str(e)
  exitState = UNKNOWN

print rtnMsg
raise SystemExit, exitState 
