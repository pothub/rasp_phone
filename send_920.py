import sys
import binascii

f = open(sys.argv[1], 'rb')
send_bin = f.read()
f.close()

send_len_int = len(send_bin) -3
print send_len_int
if send_len_int >= 2034:
    print "2034"
    sys.exit()
send_len_format = '%04x' % send_len_int
print send_len_format
send_len_bin = binascii.unhexlify(str(send_len_format))
transmit_bin = "sendb=" + send_len_bin + send_bin[:-3] + "\n"
ff = open('/dev/ttyUSB1','wb')
# ff = open('dust.bin','wb')
ff.write(transmit_bin)
print transmit_bin
ff.close()
