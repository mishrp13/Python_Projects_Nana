#!/bin/bash

FilePath= "/home/pauk/text.csv"

if [[ -f $FilePath ]]
then
   echo "File Exist"
else
   echo "File not exist"
   exit 1
fi

# start from 3:12

