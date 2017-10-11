# -*- coding: utf-8 -*-
import math 
import wave
import numpy as np
import struct
from matplotlib import pylab as plt
import Player
import Sampler
# サイン波を生成する
class Sin:
    def __init__(self): self.__wave = []
    @property
    def Wave(self): return self.__wave
    """
    サイン波を生成する。
    a:   振幅
    fs:  サンプリング周波数
    f0:  周波数
    sec: 秒
    """
    def Create(self, a=1, fs=8000, f0=440, sec=5):
        if fs < 2*f0:
            print('サンプリング定理によると	、サンプリング周波数は周波数の2倍以上でないと元の信号を再現できない。fs={}をfs={}に強制変換する。'.format(fs, 2*f0))
            fs = 2*f0
        self.__wave.clear()
        for n in np.arange(fs * sec):
            s = a * np.sin(2.0 * np.pi * f0 * n / fs) # サンプリング(標本化)する
            self.__wave.append(s)
        return self.__wave

#十二平均律
class EqualTemperament:
    def __init__(self):
        self.__names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        self.__diffs = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2]
        self.__frequencies = {}
        self.__CreateFrequencies()
    def __CreateFrequencies(self):
        for key, diff in zip(self.__names, self.__diffs):
            self.__frequencies[key] = 440 * math.pow(2, diff * (1/12.0))
    def CreateFrequency(self, key_name):
        if key_name in self.__frequencies: return self.__frequencies[key_name]
        else: raise Exception('そのキーは存在しません。')
    @property
    def Keys(self): return self.__names
    @property
    def Frequencies(self): return self.__frequencies


if __name__ == "__main__" :
    et = EqualTemperament()
    s = Sin()
    sampler = Sampler.Sampler()

    """
    # 音声データ結合
    binwaves = []
    for key, f0 in et.Frequencies.items():
        print(key, f0)
        s.Create(a=1, fs=8000, f0=f0, sec=0.25)
        binwaves.append(sampler.Sampling(s.Wave))
    print('1回目')
    p = Player.Player()
    p.Open()
    p.Play(b''.join(binwaves))
    p.Close()
    print('2回目')
    p0 = Player.Player()
    p0.Open()
    p0.Play(b''.join(binwaves))
    p0.Close()
    """
    # 音声データ単体
    p = Player.Player()
    p.Open()
    for key, f0 in et.Frequencies.items():
        print(key, f0)
        s.Create(a=1, fs=8000, f0=f0, sec=0.5)
        p.Play(sampler.Sampling(s.Wave))
    p.Close()
