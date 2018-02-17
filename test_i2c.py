import smbus
import time
from copy import deepcopy

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

CMD_LAST_CHUNK = 0x00
CMD_INTERMEDIATE_CHUNK = 0x01
CMD_GET_TOUCH_CMD = 0x10

def sendString(value):
    try :
        print value
        chunks = StringToBytes(value)
        #print chunks
        nchunk = 0
        for chunk in chunks :
            # not last chunk
            cmd = CMD_INTERMEDIATE_CHUNK
            if (nchunk == (len(chunks) - 1)) :
                # last chunk
                cmd = CMD_LAST_CHUNK
            #print str(nchunk)+" of "+str(len(chunks))+": "+str(chunk)
            bus.write_i2c_block_data(address, cmd, chunk)
            time.sleep(0.5)
            #resp = bus.read_i2c_block_data(address, 0)
            #number = readNumber()
            #print "Sent "+str(len(chunk))+" received "+str(number)
            nchunk += 1
        time.sleep(1)
        print "Waiting for response..."
        resp = bus.read_i2c_block_data(address, 0)
        while (resp is None) :
            resp = bus.read_i2c_block_data(address, 0)
        print "Got response: "+str(resp)+" = "+BytesToString(resp)
    except IOError as e:
        return 0

def sendCmd(cmd):
    try :
        #resp = bus.read_i2c_block_data(address, cmd)
        #resp = bus.read_byte_data(address, cmd)
        resp = bus.read_i2c_block_data(address, cmd, 1)
        return resp
    except IOError as e:
        return 0

def BytesToString(val):
    retVal = ''
    for c in val:
        if c != 255 :
            retVal += chr(c)
    return retVal

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
    #var = '{"cmd":"getTouchCmd", "idCmdMaster":"12", "idCmdSlave":"0", "status":"0", "response":""}'
    #sendString(var)
    resp = sendCmd(CMD_GET_TOUCH_CMD)
    #print str(type(resp))
    if resp is not None and isinstance(resp, list) and len(resp) > 0 : 
        resp = int(chr(int(resp[0])))
    if (resp > 0) :
        print str(resp)
    #time.sleep(0.1)

    #number = readNumber()
    #print "Arduino: Hey RPI, I received a digit ", number
    #print
