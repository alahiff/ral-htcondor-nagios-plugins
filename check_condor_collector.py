#!/usr/bin/python

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
