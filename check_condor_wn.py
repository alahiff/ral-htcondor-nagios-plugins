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
import math
import optparse

# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

rtnMsg = ""
exitState = OK

parser = optparse.OptionParser()
parser.add_option("-w", dest="wn", help="Minimum acceptable number of WNs advertised")
parser.add_option("-o", dest="online", help="Minimum acceptable percentage of online WNs")

(option, args) = parser.parse_args()

if option.wn:
 minWorkerNodes = option.wn
else:
 minWorkerNodes = 80

if option.online:
 minOnLine = option.online
else:
 minOnLine = 70

try:
  coll = htcondor.Collector(socket.gethostname())
  startds = coll.query(htcondor.AdTypes.Startd, "PartitionableSlot =?=TRUE", ["StartJobs", "NODE_IS_HEALTHY"])
  count = 0
  for startd in startds:
   if str(startd["StartJobs"]) != "False" and str(startd["NODE_IS_HEALTHY"]) == "True":
    count += 1
  percentOnLine = math.ceil((float(count)/len(startds)*100.0)*100)/100

  if len(startds) < minWorkerNodes:
    rtnMsg = 'WNs advertised => ' + str(len(startds)) + ' [Required => ' + str(minWorkerNodes) + ']. '
    exitState = CRITICAL

  if percentOnLine < minOnLine:
   rtnMsg += 'WNs online => ' + str(percentOnLine) + '% of advertised [Required => ' + str(minOnLine) + '%]. '
   exitState = CRITICAL

  if exitState is 0:
   rtnMsg += 'OK: ' +str(len(startds)) + ' workers are being advertised. ' + str(percentOnLine) + '% of them are online' 
 
except Exception,e:
    rtnMsg = "UNKNOWN: Problem running check. " + str(e)
    exitState = UNKNOWN

print rtnMsg
raise SystemExit, exitState

