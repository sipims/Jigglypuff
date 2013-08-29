#/bin/bash

for (( i=0; i<10; i++)) do
    cp mono_levelled.wav mono.wav
    sh run.sh mono.wav
    minimodem -r 100 -M 800 -S 600 -f mono_levelled.wav
done
