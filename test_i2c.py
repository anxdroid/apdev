import smbus
import time
from copy import deepcopy

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeString(value):
    try :
        print value
        chunks = StringToBytes(value)
        #print chunks
        nchunk = 0
        for chunk in chunks :
            # not last chunk
            cmd = 0x01
            if (nchunk == (len(chunks) - 1)) :
                # last chunk
                cmd = 0x00
            print str(nchunk)+" of "+str(len(chunks))+": "+str(chunk)
            bus.write_i2c_block_data(address, cmd, chunk)
            time.sleep(0.2)
            #resp = bus.read_i2c_block_data(address, 0)
            #number = readNumber()
            #print "Sent "+str(len(chunk))+" received "+str(number)
            nchunk += 1
    except IOError as e:
        return 0

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    try :
        number = bus.read_byte(address)
        # number = bus.read_byte_data(address, 1)
        return number
    except IOError as e:
        return 0

def StringToBytes(val):
    retVal = []
    count = 0
    chunk = []
    for c in val:
        if (count % 31 == 0) :
            if (count > 0) :
                #print "New chunk at "+c
                #print str(len(chunk))+" bytes"
                retVal.append(deepcopy(chunk))
            chunk = []
        count += 1
        #print c+": "+str(ord(c))
        chunk.append(ord(c))
    #print "To be added "+str(len(chunk))
    if (len(chunk) > 0) :
        #print str(len(chunk))+" bytes"
        retVal.append(deepcopy(chunk))
    
    print "Found "+str(len(retVal))+" chunks"
    return retVal

while True:
    #var = input("Enter 1 - 9: ")
    #if not var:
    #    continue
    var = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}"
    writeString(var)
    #print "RPI: Hi Arduino, I sent you ", var
    # sleep one second
    time.sleep(50)

    #number = readNumber()
    #print "Arduino: Hey RPI, I received a digit ", number
    #print
