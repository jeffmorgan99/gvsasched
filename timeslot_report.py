#!/usr/bin/python3
import datetime
import sys

seas_start = datetime.datetime(2022,5,2)
seas_end =  datetime.datetime(2022,7,29)

print("Opening Day: " + seas_start.strftime("%a %-m/%-d"))
print("Last Day   : " + seas_end.strftime("%a %-m/%-d"))

gamecounts = {}
day = seas_start
while day <= seas_end:
    for time in ["6", "7", "8", "1"]:
        for field in ["1", "2", "3", "4", "5"]:
            slotname = "%s:%s|%s" % (day.strftime("%-m/%-d"), time, field)
            gamecounts[slotname] = 0
    day =  day + datetime.timedelta(days=1)

# read in the master file
f = open("mastersched.csv","r")
lines = f.readlines()
for line in lines:
    c_fields = line.split(",")

    month = c_fields[1][4:5] 
    day = c_fields[1].split("/")[1]

    time = c_fields[2][0]

    t1 = c_fields[3]
    t2 = c_fields[4]
    field = c_fields[5][6:7]


    slotname = "%s/%s:%s|%s" %(month, day, time, field)

    if slotname not in gamecounts.keys():
        print("===============================")
        print("ERROR PARSING")
        print(line)
        print(slotname)

        print(month)
        print(day)
        print(time)
        print(t1)
        print(t2)
        print(field)
        for key in gamecounts.keys():
            print(key)
        sys.exit()
    gamecounts[slotname] = gamecounts[slotname] + 1

day = seas_start
print("+----------+------------+------------+------------+------------+")
print("|          | 6:15       | 7:30       | 8:45       | 10:00      |")
while day <= seas_end:
    if day.strftime("%a") == "Fri":
        sys.stdout.write("| " + day.strftime("%a %-m/%d") + " | ")
        dayinc = 3

    elif day.strftime("%a") == "Mon":
        print("+----------+------------+------------+------------+------------+")
        sys.stdout.write("| " + day.strftime("%a %-m/%d") + " | ")
        dayinc = 1
    else:
        sys.stdout.write("| " + day.strftime("%a %-m/%d") + " | ")
        dayinc = 1

    for time in ["6", "7", "8", "1"]:
        for field in ["1", "2", "3", "4", "5"]:
            slotname = "%s:%s|%s" % (day.strftime("%-m/%-d"), time, field)
            sys.stdout.write("%i " %gamecounts[slotname])
        sys.stdout.write(" | ")
    day =  day + datetime.timedelta(days=dayinc)
    print("")
print("+----------+------------+------------+------------+------------+\n")
