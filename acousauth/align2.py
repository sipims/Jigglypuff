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


def cut_series(series, start, window, amph, ampl):
    for i in xrange(0, len(series), window):
        if all(map(lambda x: abs(x)<=amph and abs(x)>=ampl,
                   series[i:i+window])):
            return i

    return None


def decrease_series(series):
    for x in xrange(len(series)-1):
        if series[x] < series[x+1]:
            return False

    return True


def increase_series(series):
    for x in xrange(len(series)-1):
        if series[x] > series[x+1]:
            return False

    return True


def find_pole(series, start, window, delta, amp):
    mid = window / 2
    left = int(mid - delta * window)
    right = int(mid + delta * window)
    for i in xrange(start, len(series)):
        subs = series[i:i+window]
        pole = min(subs)

        if pole >= 1 or abs(pole)<amp:
            continue

        for k in xrange(left, min(right, window-1)):
            if subs[k] == pole:
#                if decrease_series(subs[max(k-1, 0):k]) and \
#                   increase_series(subs[k:min(k+1, window)]):
                    return pole, i+k, i+1

    return None, start+1, start+1





def detect_period_seq(series, **kwargs):
    window = kwargs.get("window", 50)
    gap_thresh = kwargs.get("gap_thresh", 25)
    n_detected = kwargs.get("n_detected", 20)
    delta = kwargs.get("delta", 0.1)
    amp = kwargs.get("amp", 100)
    pole0, pos0, left = find_pole(series, 0, window, delta, amp)
    m = [pos0]
    pole0, pos0, left = find_pole(series, pos0, window, delta, amp)
    m.append(pos0)

    gap = m[1] - m[0]

    while (left<len(series)):
        pole1, pos1, left = find_pole(series, pos0, window, delta, amp)

        if pole1:
            gap1 = pos1 - pos0

            if abs(gap1 - gap) <= gap_thresh:
                m.append(pos1)
            else:
                m = [pos0]

            pos0 = pos1
            gap = gap1

        if len(m) >= n_detected:
            __log__(m)
            return m


def get_wave_align(w1, w2):
    s1 = detect_period_seq(w1.array)[0]
    s2 = detect_period_seq(w2.array)[0]

    return (s2 - s1) * 2


def make_wave_file(series, params, name):
    out = wave.open(name, "w")
    out.setparams(params)
    out.writeframes(series)
    out.close()


if __name__ == "__main__":
    w1 = WaveData("noise.wav")
    w2 = WaveData("mono.wav")

    default_cut = 3000
    cut_pos = cut_series(w2.array[default_cut:], 0, 20, 2100, 0)

    cut_pos += default_cut+1

    s1 = detect_period_seq(w1.array)[15]
    m2 = detect_period_seq(w2.array[cut_pos+1:])

    s2 = m2[15]

    delta = ((m2[15] - m2[10] + m2[14] - m2[9] + m2[13] - m2[8]) / 5) / 3
    __log__(delta, s1, s2)



    end = 95000
    mins = 99999999999999999999
    new_start = -1

    for i in xrange(-15, 15):
        start = s2+2+cut_pos+delta*i
        num = end - start + 1

        changed = sum(map(lambda x,y: 1 if abs(x-y)<abs(x) else 0,
                          w2.array[start+5000:end], w1.array[s1+1+5000:s1+num]))

        if changed < mins:
            new_start = start * 2 - delta*2
            mins = changed
            __log__("New start: ", new_start, mins)

    ss1 = detect_period_seq(w1.array[s1+1:])[0]
    ss2 = detect_period_seq(w2.array[new_start/2:])[0]

    make_wave_file(w1.data[s1*2+2+ss1*2:], w1.params, "noise_1.wav")
    make_wave_file(w2.data[new_start+ss2*2:], w2.params, "mono_1.wav")

    if DEBUG:
        make_wave_file(w1.data[:s1*2+ss1*2], w1.params, "noise_debug.wav")
        make_wave_file(w2.data[:new_start+ss2*2], w1.params, "mono_debug.wav")
