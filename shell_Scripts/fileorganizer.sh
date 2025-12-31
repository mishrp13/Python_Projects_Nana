# !/bin/bash

echo " ==File Organizer== "

echo "creating test files...."

touch document{1..3}.txt

touch photo{1..3}.jpg

touch data{1..3}.csv

touch script{1..3}.sh

# create directories

mkdir -p documents images data scripts

# count and move files

txt_count=$(ls *.txt 2>/dev/null | wc -l)
jpg_count=$(ls *.jpg 2>/dev/null | wc -l)
csv_count=$(ls *.csv 2>/dev/null | wc -l)
sh_count=$(ls *.sh 2>/dev/null | wc -l)

echo ""

echo "Found files"

echo "Text files: $txt_count"
echo "Jpg files: $jpg_count"
echo "Csv files: $csv_count"
echo "Sh files: $sh_count"

# Move files

[ $txt_count -gt 0 ] && mv *.txt documents/
[ $jpg_count -gt 0 ] && mv *.jpg images/
[ $csv_count -gt 0 ] && mv *.csv data/
[ $sh_count -gt 0 ]  && mv *.sh scripts/

echo ""


echo "Files organized:"

ls -R documents/ images/ data/ scripts/

#cleanup


echo ""

read -p "Remove organized directories? (y/n) " answer
if [ "$answer" == "y" ]; then
   rm -rf documents/ images/ data/ scripts/
   echo "cleaned up"
fi


