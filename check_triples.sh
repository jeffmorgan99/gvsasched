#!/bin/bash
./gamereport.py | egrep -v "^1|^2" | head -n 5
./gamereport.py | egrep --color "678|689|691|671|681|789|781|791|891"
echo
