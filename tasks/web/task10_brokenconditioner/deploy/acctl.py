#!/usr/bin/env python

import sys

if len(sys.argv) != 4:
    print("Usage: {} <temp> <room_id> <ac_id>".format(sys.argv[0]))
    exit(0)

try:
    temp    = sys.argv[1]
    room_id = int(sys.argv[2])
    ac_id   = int(sys.argv[3])

    if room_id < 1 or room_id > 1001:
        print("[acctl][Error] Bad room number")
        exit(0)

    if ac_id % room_id < 5: 
        print("[acctl][Error] Bad pin code for room #{}".format(room_id))
        exit(0)

    print("[acctl][OK] Set temperature {}\u00b0C to AC with ID #{} at room #{}".format(temp, ac_id, room_id))

except:
    print("[acctl][Error] Error, process closed")