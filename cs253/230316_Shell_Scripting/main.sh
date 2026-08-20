#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <output_file> <log_file>"
    exit 1
fi

input_file=$1
output_file=$2
log_file=$3

echo "$(date '+%Y-%m-%d %H:%M:%S') - Script execution started" > "$log_file"

if [ ! -f "$input_file" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: Input file not found!" >> "$log_file"
    exit 1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Input file exists" >> "$log_file"

# Extract unique IPs
awk -F, 'NR>1 {print $1}' "$input_file" | sort | uniq > "$output_file"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Unique IP extraction completed" >> "$log_file"

# Top 3 HTTP methods
awk -F, 'NR>1 {count[$3]++} END {for (m in count) print count[m], m}' "$input_file" | sort -nr | head -3 >> "$output_file"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Top 3 HTTP methods identified" >> "$log_file"

# Fixed: Count requests per hour
awk -F, 'NR>1 {split($2, parts, ":"); hour=substr(parts[1],12,2); hour_count[hour]++} END {for (h=0; h<24; h++) printf "Hour %02d: %d requests\n", h, hour_count[h]+0}' "$input_file" >> "$output_file"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Hourly request count completed" >> "$log_file"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Script execution completed" >> "$log_file"
