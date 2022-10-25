#!/bin/bash
./gamereport.py | egrep -v "^1|^2" | head -n 5
./gamereport.py | egrep --color 61
echo
