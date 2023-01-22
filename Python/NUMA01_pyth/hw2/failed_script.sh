#!/bin/bash

arg=$1

# Check which task we want to run
if [ $arg -eq 3 ]; then
    echo ""
    echo "Checking task 3 [that Interval[1,2] outputs [1,2]]"
    python3 -c "from hw import *; sys.stdout.write[repr[Interval[1,2]]]; print['\n']"
#elif[ $arg -eq 4 ]
#    echo ""
#    echo ""
#    exit 0
else
    echo "Woho! task 4 is so fun :)"
    #echo "Error! \"$1\" is not a valid argument."
fi
