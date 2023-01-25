#!/bin/bash
mkdir temp
for i in {0..1000000}
do
    wget -q http://192.168.0.103:8060/query/icon/$i -O temp/chan$i.jpeg
    if [ $(expr $i % 1000) == "0" ]
    then
        echo $i
        find temp/ -size 0 -exec rm {} \;
        find temp/ ! -size 0 -print
    fi
done
find temp/ -size 0 -exec rm {} \;
