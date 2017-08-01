import serial
import pygame.mixer
import time
import shutil

recv_file = "recv.mp3"
copy_file = "copy.mp3"
ser = serial.Serial('/dev/ttyUSB0', 38400)

cycle_num = 200

for num in range(cycle_num):
    readline = lambda : iter(lambda:ser.read(1),"\n")
    while "".join(readline()) != "<<SENDFILE>>":
        pass
    print "recv start"
    start = time.time()
    with open(recv_file,"wb") as outfile:
        while True:
            line = "".join(readline())
            if line == "<<EOF>>":
                break
            print >> outfile,line
    print "recv end"
    elapsed_lime = time.time() - start
    print str(elapsed_lime)
    shutil.copy(recv_file, copy_file)
    f = open('watchdog_flag','w')
    f.close()
