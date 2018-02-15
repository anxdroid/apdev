import serial
from time import sleep, time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5, 
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS)

#while 1:
#    line = ser.readline()
#    print(line)

ser.isOpen()

while 1:
    ser.write("test")
    print("sent..")
    sleep(5)

ser.close()

