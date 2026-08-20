#!/bin/bash

# Combined argument and file existence check
if [[ $# -ne 2 || ! -f "$1" || ! -f "$2" ]]; then
    echo "Usage: $0 <file1> <file2>"
    echo "Both input files must exist."
    exit 1
fi

output="prefix_lengths.txt"
> "$output"  # Clear output file

# Function to calculate common prefix length
common_prefix_length() {
    local str1="$1"
    local str2="$2"
    local len1=${#str1}
    local len2=${#str2}
    local min_len=$(( len1 < len2 ? len1 : len2 ))
    local i=0

    while [[ $i -lt $min_len && "${str1:$i:1}" == "${str2:$i:1}" ]]; do
        ((i++))
    done

    echo "$i"
}

# Main processing
exec 3<"$1"  # Open file1 on descriptor 3
exec 4<"$2"  # Open file2 on descriptor 4

while true; do
    read -r line1 <&3 || line1=""
    read -r line2 <&4 || line2=""

    if [[ -z "$line1" && -z "$line2" ]]; then
        break
    fi

    common_length=$(common_prefix_length "$line1" "$line2")
    echo "$common_length" >> "$output"
done

# Close file descriptors
exec 3<&-
exec 4<&-

echo "Success! Results in $output"
