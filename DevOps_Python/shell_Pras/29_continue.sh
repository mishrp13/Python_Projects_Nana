#!/bin/bash

for i in {1..9}

do
   let r=$i%2
   if [[ $r -eq 0 ]]
   then 
       continue
   fi
   echo "odd number is $i"
done

