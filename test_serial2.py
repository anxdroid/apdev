import serial
from time import sleep, time

ser = serial.Serial('/dev/ttyUSB0', 9600, 
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	timeout=5,
	xonxoff=0,
	rtscts=0)

if(ser.isOpen() == False):
    ser.open()

ser.setDTR(False)
ser.flushInput()
sleep(1)
ser.setDTR(True)

while 1:
    ser.write("Xxx\n")
    print("sent..")
    sleep(2)

ser.close()

