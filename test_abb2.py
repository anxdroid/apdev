import blynklib
from blynktimer import Timer
import argparse
import re
import time
import logging
import sys
import httplib2
import hashlib
import json

current_milli_time = lambda: int(round(time.time() * 1000))

authToken = "KM9LzlVrspRUZdElncYiDhWUgR0OlgjA"
port = 8080
ip = "192.168.1.9"
blynk = blynklib.Blynk(authToken, server=ip, port=port, heartbeat=30)
timer = Timer()

feeds = [
    {
        "name" : "m64061_1_YearWH",
        "vpin" : "7"
    },
    {
        "name" : "m64061_1_MonthWH",
        "vpin" : "6"
    },
    {
        "name" : "m64061_1_WeekWH",
        "vpin" : 5
    },  
    {
        "name" : "m101_1_PhVphA",
        "vpin" : 4
    },
    {
        "name" : "m101_1_A",
        "vpin" : 3
    },
    {
        "name" : 'm64061_1_DayWH',
        "vpin" : 2
    },
    {
        "name" : 'm101_1_W',
        "vpin" : 1
    }
]

CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'

@blynk.handle_event("connect")
def connect_handler():
    print(CONNECT_PRINT_MSG)

@blynk.handle_event("disconnect")
def disconnect_handler():
    print(DISCONNECT_PRINT_MSG)
    blynk.connect()

@timer.register(interval=5)
def readVal():
    abb = APABB("192.168.1.154", "admin", "db6e106cf2b982d8dce1cf2ba2e0d449", "Thejedi82", "4:120399-3G96-3016")
    for feed in feeds :
        try:
            print("Polling from "+feed["name"]+" on vpin "+str(feed["vpin"]))
            val = abb.fetch(feed["name"])
            if (val is not None) :
                blynk.virtual_write(feed["vpin"], str(val))
        except Exception as e:
            print (e)

class APABB(object):
    nonce = None
    challenge = None
    username = None
    HA1 = None
    nc = "00000002"
    cnonce = "ddf4bfcaf87acba9"
    qop = "auth"
    HA2 = None
    password = None
    response = None
    host = None
    debug = False
    resp = None
    userToken = None
    respHeaders = None

    def __init__(self, host, username, userToken, password, ser) :
        self.host = host
        self.username = username
        self.password = password
        self.ser = ser
        self.userToken = userToken
        #self.debug = True
        self.cookies = None

    def extractNonce(self) :
        timestamp = str(int(time.time()))
        #if self.debug :
        #    print(self.respHeaders)
        if ("www-authenticate" in self.respHeaders and self.respHeaders["www-authenticate"] is not None) :
            regexp = re.search("nonce=\"([^\"]+)\"", self.respHeaders["www-authenticate"])
            if (regexp is not None) :
                self.nonce = str(regexp.group(1))
    
    def handleAuth(self, path) :
        self.HA1 = self.userToken

        if self.debug:
            print ("Nonce: "+self.nonce)
        
        """
        if self.debug:
            print ("Path: "+path)
        """

        HA2_md5 = hashlib.md5()
        HA2Val = "GET:"+path
        HA2_md5.update(HA2Val.encode('utf-8'))
        self.HA2 = HA2_md5.hexdigest()
        
        if self.debug:
            #print ("HA1: "+self.HA1)
            print ("HA2: "+self.HA2)
        
        response_md5 = hashlib.md5()
        responseVal = self.HA1+":"+self.nonce+":"+self.nc+":"+self.cnonce+":"+self.qop+":"+self.HA2
        response_md5.update(responseVal.encode('utf-8'))
        self.response = response_md5.hexdigest()
        
        """
        if self.debug:
            print ("Response: "+self.response)
        """

    def buildReq(self, path, method, timestamp) :
        conn = httplib2.Http()
        headers = {}
        """
GET /v1/feeds/ser4:120399-3G96-3016/datastreams/m101_1_W?_=1574854636192 HTTP/1.1
Host: 127.0.0.1:10480
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: application/json, text/plain, */*
Authorization: X-Digest username="admin", realm="registered_user@power-one.com", nonce="937e6a2a189cfe3791f4bd0a2cd852fe", uri="/v1/feeds/ser4:120399-3G96-3016/datastreams/m101_1_W?_=1574854636192", response="a7a24c8e57ccb4266be5356c4bea2ba0", qop=auth, nc=00000002, cnonce="ddf4bfcaf87acba9"
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Referer: http://127.0.0.1:10480/v3/
Accept-Encoding: gzip, deflate, br
Accept-Language: it-IT,it;q=0.9,en;q=0.8,es;q=0.7,pl;q=0.6
Cookie: _ga=GA1.1.169258567.1574776814; _gid=GA1.1.932969922.1574776814; _gat=1
        """    
        headers = {
            "Cookie": 'auth.method="GET";auth.challenge="X-Digest realm=\"registered_user@power-one.com\", nonce=\"937e6a2a189cfe3791f4bd0a2cd852fe\", qop=\"auth\"";auth.user={"id":"admin","authToken":"db6e106cf2b982d8dce1cf2ba2e0d449"};auth.uri="../au/logger/v1/wifi/status?_=1574860320060";_ga=GA1.1.169258567.1574776814;_gid=GA1.1.932969922.1574776814',
            "Connection": "keep-alive",
            "Pragma": "no-cache",
	    "Cache-Control": "no-cache",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8,es;q=0.7",
	    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
	    "Sec-Fetch-Site": "same-origin",
	    "Sec-Fetch-Mode": "cors",
	    "Referer": "http://"+self.host+"/v3/"}
        if (self.nonce is not None) :
            self.handleAuth(path)
            headers["Authorization"] = "X-Digest username=\""+self.username+"\", realm=\"registered_user@power-one.com\", nonce=\""+self.nonce+"\", uri=\""+path+"\", response=\""+self.response+"\", qop="+self.qop+", nc="+self.nc+", cnonce=\""+self.cnonce+"\""
        if (self.cookies is not None) :
            headers['Cookie'] = self.cookies
        if self.debug :
            print(headers)
        #if self.debug:
            #print ("Auth: "+str(headers["Authorization"]))
        try :
            myUri = "http://"+self.host+path
            if self.debug:
                print ("Connecting to "+myUri+"...")
            (respHeaders, resp) = conn.request(myUri, method, headers=headers)
            self.respHeaders = respHeaders
            self.resp = str(resp.decode("utf-8"))
            if self.debug:
                print ("Status: "+respHeaders["status"])
            if self.debug:
                print(respHeaders)
            if ('set-cookie' in respHeaders) :
                self.cookies = respHeaders['set-cookie']
            #if (self.debug) :
            #    print(self.cookies)
            return True
        except Exception as e:
            print ("HTTP error: " + str(e))
        return None

    def callUrl(self, uri) :
        timestamp = str(int(time.time()))
        self.buildReq(uri, "GET", timestamp)
        if (self.debug) :
            print(uri)
        if self.resp is None :
            return None
        else :
            self.extractNonce()
        if (self.debug) :
            print("==============================")
    
    def login(self) :
        #print("Logging in...")
        uri = "/v3/"
        self.callUrl(uri)
        timestamp = str(current_milli_time())
        uri = "/v1/status?_="+timestamp
        self.callUrl(uri)
        self.callUrl(uri)

        uri = "/au/logger/v1/public_config"
        self.callUrl(uri)

        uri = "/v1/config"
        self.callUrl(uri)

    def fetch(self, feed) :
        #print("Fetching data...")
        if self.nonce is None :
            self.login()
            if self.nonce is None :
                return None

        timestamp = str(current_milli_time())
        uri = "/v1/feeds/ser"+self.ser+"/datastreams/"+feed+"?_="+timestamp
        self.callUrl(uri)
        try:  
            payload = json.loads(self.resp)
            if (self.debug) : 
                print(payload)
            if payload is not None and 'feeds' in payload and 'ser'+self.ser in payload["feeds"]:
                datastreams = payload['feeds']['ser'+self.ser]['datastreams']
                lastVal = datastreams[feed]['data'][0]
                units = datastreams[feed]['units']
                if (lastVal is not None) :
                    print(str(lastVal["value"])+" "+units)
                    return lastVal["value"]
                else :
                    print ("No value found !")
        except ValueError as e:
            print("JSON error: "+str(e))
        print("---------------------------------------------------------")
        return None  


def main():
    #sys.stdout = open("/var/log/domotic.log", "w", buffering=2)
    #abb = APABB("192.168.1.154", "admin", "db6e106cf2b982d8dce1cf2ba2e0d449", "Thejedi82", "4:120399-3G97-3016")
    #abb.fetch('m64061_1_DayWH')
    while True:
        blynk.run()
        timer.run()

if __name__ == "__main__":
		main()
