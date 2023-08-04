#!/bin/bash


for i in 1 2 3 4 5 6
  do
   echo $i
  done

for j in $(ls)
 do 
   echo $j
 done

sum=0
for((i=1;i<100;i=i+1))
 do 
  sum=$(($sum+$i))
  echo $i
 done
echo "sum,$sum"

