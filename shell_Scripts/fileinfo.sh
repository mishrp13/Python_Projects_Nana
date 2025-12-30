# !/bin/bash

# validate the argument

if [ $# -eq 0 ]; then
   echo "Usage :$0 <filename>"
   exit 1

fi

file=$1

#check if file exists

if [ ! -f "$file" ]; then
   echo "Error: file '$file' not found "
   exit 1
fi

# Display the information

echo "  == File Information ==  "

echo "Name: $(basename "$file")"
echo "Path: $(realpath "$file")"
echo "Size: $(wc -c <"$file") bytes"
echo "Lines: $(wc -l <"$file")"
echo "Words: $(wc -w <"$file")"


# check permission

echo ""

echo "== Permissions =="

[ -r "$file" ] && echo " Readable " || echo "Not readable"
[ -w "$file" ] && echo " Writable " || echo " Not writable "
[ -x "$file" ] && echo " Executable " || echo " Not executable "


echo ""

echo "Last modified: $(date -r "$file")"









