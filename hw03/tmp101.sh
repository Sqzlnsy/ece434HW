#!/bin/sh
i2cbus=$1
shift
while([ "1" = "1" ]) do
    for i2cAddr in $@ 
    do
        temp=`i2cget -y ${i2cbus} ${i2cAddr} 00`
        temp=$(($temp * 9/5+32))
        echo -n "temp at ${i2cAddr}: ${temp} F; \\t"
        sleep 0.5
    done
    echo -n "\\r"
done