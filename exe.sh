#!/bin/bash
./scaleAudio.py -i=$1 -o=example.wav -t=phasevocoder -s=0.5

# i = input wav file name
# o = output wav file name
# t = time modulation type | ola - wsola - phasevocoder
# s = speed modulation | above 1 speeds up, below 1 slows down 
    # - for example: 2 doubles the speed, 0.5 halves the speed

# to review the paper detailing the different algorithms implemented here:
# https://www.mdpi.com/2076-3417/6/2/57/htm