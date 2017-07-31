import serial
import sys      # for argv

print "serial communication start"

argv = sys.argv
argc = len(argv)

if(argc != 3):
    print 'Usage: python %s arg1 arg2' %argv[0]
    print 'arg1 is "r" or "s"'
    print "r:mode recv, s:mode send"
    print "arg2 is baud rate to communicate other module"
    quit()

ser = serial.Serial('/dev/ttyUSB0', int(argv[2]))
if(argv[1] == "r"):
    print "mode r"
    # c = ser.read()
    line = ser.readline()
    print line
elif(argv[1] == "s"):
    print "mode s"
    ser.write("communication_test\n")

ser.close()

