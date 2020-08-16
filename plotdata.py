import pyaudio
from effects import *
import matplotlib.pyplot as plt
import numpy as np
import time

p = pyaudio.PyAudio()

CHANNELS = 1
RATE = 44100
data = None

def callback(in_data, frame_count, time_info, flag):
    global data
    data = np.frombuffer(in_data,dtype=np.float32)
    return data, pyaudio.paAbort

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(1)
    stream.stop_stream()
    print("Stream is stopped")
stream.close()
p.terminate()

average = np.average(data)
std = np.std(data)
maxVal = np.max(data)
minVal = np.min(data)
avg2 = np.average([average,maxVal])
avg3 = np.average([average,minVal])
data = [avg2 if i >= avg2 else i for i in data]
data = [avg3 if i <= avg3 else i for i in data]

plt.plot(range(1024),[maxVal for i in range(1024)],color="red")
plt.plot(range(1024),[minVal for i in range(1024)],color="red")
plt.plot(range(1024),[average for i in range(1024)],color="blue")
plt.plot(range(1024),[average + 3*std for i in range(1024)],color="green")
plt.plot(range(1024),[average - 3*std for i in range(1024)],color="green")
plt.plot(range(1024),data)
plt.show()