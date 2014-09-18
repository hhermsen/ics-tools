#!/usr/bin/python

from icalendar import Calendar
import sys

if len(sys.argv) < 4:
    print "Usage: missing_ics_uid.py source.ics target.ics missing.ics"
    sys.exit(1)

cal_source = Calendar.from_ical(open(sys.argv[1], 'rb').read())
cal_target = Calendar.from_ical(open(sys.argv[2], 'rb').read())
cal_missing = Calendar()

for component_source in cal_source.subcomponents:
    if not component_source.has_key("UID"):
        print "*** components with no UID in source ***"
        print component_source.to_ical()

print "*** missing components with UID ***"

for component_source in cal_source.subcomponents:
    if component_source.has_key("UID"):
        for component_target in cal_target.subcomponents:
            if component_target.has_key("UID") and component_source["UID"] == component_target["UID"]:
                break
        else:
            # loop fell through without finding this UID in the target
            print component_source.to_ical()
            cal_missing.subcomponents.append(component_source)

print str(len(cal_missing.subcomponents)) + " components where missing"

f = open(sys.argv[3], 'wb')
f.write(cal_missing.to_ical())
f.close()
