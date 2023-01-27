#!/bin/bash
ROKU_DEV_TARGET=192.168.0.103
folder=temp
end=2000000
latest=""
if [ "$1" != "" ]
then
    folder=$1
fi
if [ "$2" != "" ]
then
    latest="$2"
fi
mkdir -p $folder
if [ "$latest" == "" ]
then
    latest=$(ls -t ${folder}/ | head -1 | grep -Eo "[0-9]*")
fi
start=$((latest))
echo start is $start
for (( i=${start}; i<=${end}; i++ ))
do
    wget -q http://${ROKU_DEV_TARGET}:8060/query/icon/$i -O ${folder}/chan$i.jpeg
    if [ $(expr $i % 1000) == "0" ]
    then
        echo $i
        find ${folder}/ -size 0 -exec rm {} \;
        find ${folder}/ ! -size 0 -print
    fi
done
find ${folder}/ -size 0 -exec rm {} \;
