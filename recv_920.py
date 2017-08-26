import serial
import os
ser = serial.Serial('/dev/ttyUSB0',115200)
ser.write("listen\n")
print ser.read(5)
file_flag = 0
while 1:
    line = ser.readline()
    if line.find("RSSI") >= 0:
        print "end"
        file_flag = 0
        f.close()
        os.system("cp recv.bin copy.mp3")
        os.system("mpg321 copy.mp3 &")
    if file_flag == 1:
        # print line
        f.write(line)

    if line.find("recvb=") >=0:
        os.system("rm recv.bin")
        print "start"
        file_flag = 1
        # print line[8:]
        f = open('recv.bin','ab')
	f.write(line[8:])
