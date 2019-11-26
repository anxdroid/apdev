import blynklib
from blynktimer import Timer
import argparse
import re
import time
import logging
import sys
import httplib, urllib

authToken = ""
port = 8080
ip = "192.168.1.9"
blynk = blynklib.Blynk(authToken, server=ip, port=port, heartbeat=30)
timer = Timer()

devices = [
    {
        "name" : "current",
        "mac" : "58:2D:34:35:2F:02",
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

@timer.register(interval=300)
def readVal():
    print("Polling...")
    for device in devices :
        try:
            print("Polling data from "+device["name"])
            val = abb.fetch()
            blynk.virtual_write(device["vpin"], val)
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

    def __init__(self, host, username, userToken, password, ser) :
        self.host = host
        self.username = username
        self.password = password
        self.ser = ser
        self.userToken = userToken

    def extractNonce(self, headers) :
        timestamp = str(int(time.time()))
        regexp = re.search("nonce=\"([^\"]+)\"", headers)
        if (regexp is not None) :
            self.nonce = str(regexp.group(1))
    
    def handleAuth(self, path) :
        self.HA1 = self.userToken

        if self.debug:
            print "Nonce ------------------------------"
            print self.nonce
            print "------------------------------------"
        
        """
        self.challenge = 'X-Digest realm="registered_user@power-one.com", nonce="'+self.nonce+'", qop="auth"'
        
        if self.debug:
            print "Challenge --------------------------"
            print self.challenge
            print "------------------------------------"
        """

        HA2_md5 = hashlib.md5()
        HA2_md5.update(method+":"+path)
        self.HA2 = HA2_md5.hexdigest();
        
        if self.debug:
            print "HA2 --------------------------------"
            print self.HA2
            print "------------------------------------"
        
        response_md5 = hashlib.md5()
        response_md5.update(self.HA1+":"+self.nonce+":"+self.nc+":"+self.cnonce+":"+self.qop+":"+self.HA2)
        self.response = response_md5.hexdigest();
        
        if self.debug:
            print "Response ---------------------------"
            print self.response
            print "------------------------------------"

    def buildReq(self, path, method, timestamp) :
        conn = httplib.HTTPConnection(self.host)
        if self.debug:
            conn.set_debuglevel(2)

        if self.nonce is not None :
            self.handleAuth(path)
            headers = {
                "Cookie": "filter=all; _ga=GA1.3.1163095045."+timestamp+"; _gid=GA1.3.915588772."+timestamp+"; _gat=1",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "it-IT,it;q=0.9,en;q=0.8,es;q=0.7",
                "Authorization": "X-Digest username=\""+self.username+"\", realm=\"registered_user@power-one.com\", nonce=\""+self.nonce+"\", uri=\""+path+"\", response=\""+self.response+"\", qop="+self.qop+", nc="+self.nc+", cnonce=\""+self.cnonce+"\""}

        try :
            conn.request(method=method, url=path, headers=headers)
            resp = conn.getresponse()
            html = resp.read()
            headers = str(resp.msg)
            conn.close()
            return {'html':html, 'headers':headers}
        except Exception as e:
            print "HTTP error: %s" % str(e)
        return None

    def callUrl(self, uri) :
        timestamp = str(int(time.time()))
        self.resp = self.buildReq(uri, "GET", timestamp)
        if self.resp is None :
            return None
        else :
            self.extractNonce(resp['headers'])
    
    def login(self) :
        timestamp = str(int(time.time()))
        uri = "../v1/status?_="+timestamp
        self.callUrl(self, uri)
        self.callUrl(self, uri)

        uri = "/au/logger/v1/public_config"
        self.callUrl(self, uri)

        uri = "../v1/config"
        self.callUrl(self, uri)

    def fetch(self, element) :
        if self.nonce is None :
            res = self.login()
            if res is None :
                return None

        timestamp = str(int(time.time()))
        uri = "/v1/feeds/ser"+self.ser+"?_="+timestamp
        self.self.callUrl(self, uri)
        try: 
            payload = json.loads(self.resp['html'])
            if payload is not None :
                measure = payload['feeds']['ser'+self.ser]['datastreams'][element]['data'][0]
                ts = measure['timestamp']
                ts_format = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
                measure['ts'] = int(time.mktime(ts_format.timetuple())) 
                return measure
        except ValueError as e:
            print("JSON error: "+resp['html'])
        return None  
    
def main():
    sys.stdout = open("/var/log/domotic.log", "w", buffering=2)
    abb = APABB("192.168.1.154", "admin", "Thejedi82", "db6e106cf2b982d8dce1cf2ba2e0d449", "4:120399-3G96-3016")
    while True:
        blynk.run()
        timer.run()

if __name__ == "__main__":
		main()
