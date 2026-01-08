#!/bin/bash


path="C:/Users/praba/Downloads/report.txt"


echo "== original path == "

echo "$path"

echo ""

# Extract Components

filename="${path##*/}"
dirname="${path%.*}"
basename="${filename%.*}"
extension="${filename##*.}"


echo "== Components ==="

echo "Directory: $dirname"
echo "Filename: $filename"
echo "Basename: $basename"
echo "Extension: $extension"
echo ""

# Transform file name

uppercase="${filename^^}"
lowercase="${filename,,}"
renamed="${filename/report/summary}"


echo "==Transformations=="

echo "Uppercase: $uppercase"
echo "Lowercase: $lowercase"
echo "Renamed: $renamed"
echo ""

# Build new path

new_path="${dirname}/${renamed}"
echo "New path: $new_path"
echo ""

# Extract year from filename

if [[ $filename =~ ([0-9]{4}) ]]; then
   year="${BASH_REMATCH[1]}"
   echo "Found year: $year"

fi




