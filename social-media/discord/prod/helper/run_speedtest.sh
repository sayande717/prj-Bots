#!/bin/bash

# Utility: Runs an internet speed test using the specified server ID.
# Input: Speedtest Server ID
# Output: Date,time,Latency,Upload_Speed,Download_Speed

server_id=$1
# Run command
output=$(speedtest --server $server_id --simple)

# Extract values
latency=$(echo "$output" | grep '^Ping:' | awk '{print $2}')
upload=$(echo "$output" | grep '^Upload:' | awk '{print $2}')
download=$(echo "$output" | grep '^Download:' | awk '{print $2}')
date=$(date +"%d.%m.%Y")
time=$(date +"%H:%M")

# Export to CSV
echo "$date,$time,$latency,$upload,$download" >> speedtest_periodic.csv