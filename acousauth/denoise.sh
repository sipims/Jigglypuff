sox -v -1 noise_1.wav noise_rev.wav
sox -m mono_1.wav noise_rev.wav merge.wav
sox merge.wav out.wav vol $1 dB

minimodem -r 100 -M 800 -S 600 -f out.wav -c 0.5
