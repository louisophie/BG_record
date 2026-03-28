#!/bin/bash

# Read START time from stdin (or use first argument)
if [ -n "$1" ]; then
    START="$1"
else
    read -r START
fi

# Remove any extra spaces or newlines
START=$(echo "$START" | tr -d ' \t\r\n')

start_sec=$(date -d "$START today" +%s 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Invalid time format. Use HH:MM (e.g. 14:32)"
    exit 1
fi

now_sec=$(date +%s)
diff=$(( now_sec - start_sec ))

hours=$(( diff / 3600 ))
mins=$(( (diff % 3600) / 60 ))

printf "Duration from %s to now: %02d:%02d\n" "$START" "$hours" "$mins"