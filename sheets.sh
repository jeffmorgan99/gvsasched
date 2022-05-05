#!/bin/bash

# if you don't pass a date, assume it is the next Monday (unless today is Monday)

cp /dev/null sheets.csv
for date in 5/2 5/3 5/4 5/5; do
    for field in 1 2 3 4 5; do
        for time in 6:15 7:30 8:45 10:00; do
            line=$(grep " $date," mastersched.csv | grep "Field $field" | grep $time)
            div=$(echo $line | awk -F"," '{print $1}')
            home=$(echo $line | awk -F"," '{print $4}')
            away=$(echo $line | awk -F"," '{print $5}')
            echo "${date}/22,$time,"Field $field",$div,$home,$away" >> sheets.csv
        done
        echo -e "\n======,======,======,======,======,======\n" >> sheets.csv
    done
    echo "###########################" >> sheets.csv
done
