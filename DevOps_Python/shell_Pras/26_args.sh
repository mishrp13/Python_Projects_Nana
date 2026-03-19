#!/bin/bash

#to access the argument

if [[ $# -eq 0 ]]
then
    echo "Please provide one argument"
    exit 1
fi


echo "First argument is $1"
echo "Second argument is $2"

echo "All the arguments are - $@"
echo "Number of Arguments are - $#"


#For loop to acces the value from arguments

for filename in $@
do
   echo "copying file- $filename"
done

