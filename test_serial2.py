import serial
from time import sleep, time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5, 
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	timeout=1,
	xonxoff=0,
	rtscts=0)

if(ser.isOpen() == False):
	ser.open()
self.serACM.setDTR(False)
self.serACM.flushInput()
time.sleep(1)
self.serACM.setDTR(True)

while 1:
    ser.write("test")
    print("sent..")
    sleep(5)

ser.close()

