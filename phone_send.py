import pyaudio
import wave
import time

from multiprocessing import Pool
import serial
import os
import readchar

import sys,select

CHUNK = 1024 *2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1

p = pyaudio.PyAudio()
ser = serial.Serial('/dev/ttyUSB0', 38400)

def f():
    os.system("lame -b 16 record.wav record.mp3")
    print "start transfar audio data"
    ser.write("<<SENDFILE>>\n")
    readline = lambda : iter(lambda:ser.read(1),"\n")
    ser.write(open("record.mp3","rb").read())
    ser.write("\n<<EOF>>\n")
    print "end transfar audio data"

def readline_timeout(fd, timeout = 1.0):
    (r, w, e) = select.select([fd], [], [], timeout)
    if   len(r) == 0: return "a"

while True:
    pool = Pool(2)
    result = pool.apply_async(f)
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
    print("* recording")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()

    filename = "record.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    result.wait()
    if readline_timeout(sys.stdin, 0.01) != 'a':
        break


p.terminate()
