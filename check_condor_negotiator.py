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
  negotiators = coll.query(htcondor.AdTypes.Negotiator, "true", ["Name"])
  numNegotiators = len(negotiators)

  if numNegotiators >= 1:
   if numNegotiators == 1:
    rtnMsg = "Negotiator running on "
    exitState = OK 
   else:
    rtnMsg="More than 1 negotiator running "
    exitState = CRITICAL
   for negotiator in negotiators:
    rtnMsg += negotiator['Name'].replace(".gridpp.rl.ac.uk","") + " "
  else:
   rtnMsg="No negotiators running."
   exitState = CRITICAL
except Exception,e:
  rtnMsg = "Problem running check. " + str(e)
  exitState = UNKNOWN

print rtnMsg
raise SystemExit, exitState 
