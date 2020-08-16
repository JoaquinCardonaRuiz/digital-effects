import pyaudio
from effects import *
import numpy as np
import time

p = pyaudio.PyAudio()

CHANNELS = 1
RATE = 44100
board = [Overdrive()]

def callback(in_data, frame_count, time_info, flag):
    input = np.frombuffer(in_data,dtype=np.float32)
    output = input
    for fx in board:
        output = fx.activate(output)
    return output, pyaudio.paContinue

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    while True:
        corners= ["╔","╗"]
        for fx in board:
            print(corners[0]+"═"*(len(str(fx))-2)+corners[1])
            print(fx)
            corners= ["╠","╣"]
        corners= ["╚","╝"]
        print(corners[0]+"═"*(len(str(board[-1]))-2)+corners[1])

        r = input()
        if r == "q":
            break
    stream.stop_stream()
    print("Stream is stopped")

stream.close()

p.terminate()