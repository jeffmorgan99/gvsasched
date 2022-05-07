#!/bin/bash
tstamp=$(date +"%y%m%d.%H%M%S")

test -d backup || mkdir -p backup
test -f mastersched.csv && mv -v mastersched.csv backup/mastersched.$tstamp.csv

./getsched.py

diff  mastersched.csv backup/mastersched.$tstamp.csv
if [ $? -ne 0 ]; then
    diff mastersched.csv backup/mastersched.$tstamp.csv | mail -r jeffrey.morgan@oracle.com -s 'QB Site Cleanup Needed for Maintenance' -b jeffrey.morgan@oracle.com $email
fi
wc -l mastersched.csv backup/mastersched.$tstamp.csv
