#!/usr/bin/python
#-*- encoding: utf-8 -*-

import wave
import struct
import numpy

DEBUG = True

def __log__(*args):
    if DEBUG:
        print args


class WaveData:
    def __init__(self, waveFile):
        f = wave.open(waveFile)
        self.nframes = f.getnframes()
        self.data = f.readframes(self.nframes)
        self.params = f.getparams()
        self.array = [struct.unpack("h", x[0]+x[1])[0] for x in
                      zip(self.data[::2], self.data[1::2])]


def find_pole(series, start, window, delta):
    mid = window / 2
    left = int(mid - delta * window)
    right = int(mid + delta * window)
    for i in xrange(start, len(series)):
        subs = series[i:i+window]
        pole = min(subs)

        if pole >= 0:
            continue

        for k in xrange(left, right):
            if subs[k] == pole:
                return pole, i+k, i+1

    return None, start+1, start+1


def detect_period_seq(series, **kwargs):
    window = kwargs.get("window", 50)
    gap_thresh = kwargs.get("gap_thresh", 25)
    n_detected = kwargs.get("n_detected", 20)
    delta = kwargs.get("delta", 0.1)
    pole0, pos0, left = find_pole(series, 0, window, delta)
    m = [pos0]
    pole0, pos0, left = find_pole(series, pos0, window, delta)
    m.append(pos0)

    gap = m[1] - m[0]

    while (left<len(series)):
        pole1, pos1, left = find_pole(series, pos0, window, delta)

        if pole1:
            gap1 = pos1 - pos0

            if abs(gap1 - gap) <= gap_thresh:
                m.append(pos1)
            else:
                m = []

            pos0 = pos1
            gap = gap1

        if len(m) >= n_detected:
            __log__(m)
            return m


def get_wave_align(w1, w2):
    s1 = detect_period_seq(w1.array)[0]
    s2 = detect_period_seq(w2.array)[0]

    return (s2 - s1) * 2

if __name__ == "__main__":
    w1 = WaveData("noise.wav")
    w2 = WaveData("mono.wav")
    s1 = detect_period_seq(w1.array)[5]
    s2 = detect_period_seq(w2.array)[5]

    # c = [detect_period_seq(w2.array, delta=d)[0]
    #      for d in numpy.linspace(0.15, 0.25, 50)]
    # s2 = int(sum(c) / len(c))

    __log__(s1, s2)
    out1 = wave.open("noise_1.wav", "w")
    out1.setparams(w1.params)
    out1.writeframes(w1.data[0:s1*2])
    out2 = wave.open("mono_1.wav", "w")
    out2.setparams(w2.params)
    out2.writeframes(w2.data[0:s2*2])
