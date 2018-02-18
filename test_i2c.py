import smbus
import time
import urllib, json
from copy import deepcopy

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

CMD_LAST_CHUNK = 0x00
CMD_INTERMEDIATE_CHUNK = 0x01
CMD_GET_TOUCH_CMD = 0x10

API = ["", "", "", "sendSolarData", "", "", "", "", "", "", "sendTempData"]

APIKEY = "a7441c2c34fc80b6667fdb1717d1606f"
class APIs:
    url = "http://192.168.1.12/emoncms/feed/data.json?apikey="+APIKEY

    def feedToPayload(self, feedId, startTS, endTS, interval, color, justList):
        url = self.url+"&id="+str(feedId)+"&start="+str(startTS)+"&end="+str(endTS)+"&interval="+str(interval)+"&skipmissing=0&limitinterval=1"
        print url
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        payload = ""
        if (justList == False) :
            payload = "["
        index = 0;
        minTS = startTS/1000
        
        for m in data :
            if (m[1] is not None) :
                #print m
                if (index > 0) :
                    payload += ","
                #print m[0]
                offsetTS = (int(m[0])/1000) - minTS
                payload += '['+str(offsetTS)+','+("{0:.2f}".format(m[1]))
                if (color != "") :
                    payload += ',"'+color+'"'
                payload += ']'
                index += 1;
        
        if (justList == False) :
            payload += "]"
        
        return payload

    def sendSolarData(self, apiId):
        #var = '{"apiId":'+str(apiId)+', "values":["324"], "timestamps":[1112233212]}'
        #startTS = 1518700000000
        #endTS = 1518799900000
        
        endTS = ((int(time.time()) - (12*60*60)) * 1000)
        startTS = ((endTS/1000) - (6 * 60 * 60)) * 1000
        interval = 900
        payload1 = self.feedToPayload(1, startTS, endTS, interval, "Y", True)
        payload2 = self.feedToPayload(7, startTS, endTS, interval, "R", True)
        payload = '['+payload1 +','+ payload2+']'
        minTS = startTS/1000
        #print payload;
        var = '{"i":'+str(apiId)+',"s":'+str(minTS)+',"p":'+payload+'}'
        sendString(var)
    def sendTempData(self, apiId):
        #var = '{"apiId":'+str(apiId)+', "values":["324"], "timestamps":[1112233212]}'
        var = '''{"i":'''+str(apiId)+''', "p":[
        {"t":"1518974662", "v":"19.23"},
        {"t":"1518974600", "v":"19.50"}
        ]}'''
        sendString(var)

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
            #print chunk
            bus.write_i2c_block_data(address, cmd, chunk)
            time.sleep(0.1)
            nchunk += 1
        time.sleep(1)
        print "Waiting for response..."
        resp = bus.read_i2c_block_data(address, 0)
        while (resp is None) :
            resp = bus.read_i2c_block_data(address, 0)
        print "Got "+BytesToString(resp)+" bytes, sent "+value+" ["+str(len(value))+"]"
    except IOError as e:
        return 0

def sendCmd(cmd):
    try :
        resp = bus.read_i2c_block_data(address, cmd, 4)
        if resp is not None and isinstance(resp, list) and len(resp) > 0 and resp[0] != 48: 
            resp = int(BytesToString(resp))
            if resp > 0:
                return resp

    except IOError as e:
        return 0
    except ValueError as e:
        return 0
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
    
    #print "Found "+str(len(retVal))+" chunks"
    return retVal

while True:
    api = APIs()
    #var = '{"cmd":"getTouchCmd", "idCmdMaster":"12", "idCmdSlave":"0", "status":"0", "response":""}'
    #sendString(var)
    resp = sendCmd(CMD_GET_TOUCH_CMD)
    if (resp > 0) :
        print str(resp)
        print API[resp]
        if (API[resp] != "") :
            time.sleep(0.1)
            getattr(api, API[resp])(resp)
    #time.sleep(0.1)

    #number = readNumber()
    #print "Arduino: Hey RPI, I received a digit ", number
    #print
