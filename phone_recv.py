import serial
import time
import shutil
import os

ser = serial.Serial('/dev/ttyUSB0', 38400)

while True:
    readline = lambda : iter(lambda:ser.read(1),"\n")
    while "".join(readline()) != "<<SENDFILE>>":
        pass
    print "recv start"
    start = time.time()
    with open("recv.mp3","wb") as outfile:
        while True:
            line = "".join(readline())
            if line == "<<EOF>>":
                break
            print >> outfile,line
    print  "recv time:" + str(time.time() - start)
    shutil.copy("recv.mp3", "copy.mp3")
    os.system("mpg321 copy.mp3 > /dev/null 2>&1 &")
