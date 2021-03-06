import httplib, urllib
import re
import time
import datetime
import hashlib
import json


class APABB(object):
    nodeids = {"101":{"ABB_POWER_SOLAR_OUT":"W", "ABB_CURRENT_SOLAR_OUT":"A", "ABB_VOLTAGE_OUT":"V", "ABB_TEMP_INVERTER":"&deg;"}}
    domain = "192.168.1.12"
    emoncmspath = "emoncms"
    apikey = "2a4e7605bb826a82ef3a54f4ff0267ed"

    nonce = None
    challenge = None
    username = None
    # Hash of admin password
    HA1 = None
    nc = "00000002"
    cnonce = "ddf4bfcaf87acba9"
    qop = "auth"
    HA2 = None
    response = None
    host = None
    ser = None

    debug = False

    def log_emoncms(self, timestamp, nodeid, key, value):
        print(str(timestamp)+" "+str(nodeid)+" "+key+" "+str(value))
        conn = httplib.HTTPConnection(self.domain)
        url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+str(nodeid)+"&json={"+key+":"+str(value)+"}&time="+str(timestamp)
        print url
        try:
            conn.request("GET", url)
            resp = conn.getresponse()
            print resp.read()
        except Exception as e:
            print "HTTP error: %s" % str(e)

    def buildReq(self, path, method, timestamp) :
        conn = httplib.HTTPConnection(self.host)
        if self.debug:
            conn.set_debuglevel(2)
        headers = {}

        if self.nonce is not None :
            if self.debug:
                print "Nonce ------------------------------"
                print self.nonce
                print "------------------------------------"
            
            self.challenge = 'X-Digest realm="registered_user@power-one.com", nonce="'+self.nonce+'", qop="auth"'
            
            if self.debug:
                print "Challenge --------------------------"
                print self.challenge
                print "------------------------------------"

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

    def __init__(self, host, username, password, serial) :
        self.host = host
        self.username = username
        self.HA1 = password
        self.ser = serial

    def login(self) :
        timestamp = str(int(time.time()))
        uri = "/v3/#/login"
        resp = self.buildReq(uri, "GET", timestamp)

        if resp is None :
            return None

        timestamp = str(int(time.time()))
        uri = "../v1/status?_="+timestamp
        resp = self.buildReq(uri, "GET", timestamp)

        if resp is None :
            return None

        timestamp = str(int(time.time()))
        regexp1 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp1 is not None) :
            self.nonce = str(regexp1.group(1))
        resp = self.buildReq(uri, "GET", timestamp)

        if resp is None :
            return None

        timestamp = str(int(time.time()))
        regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp2 is not None) :
            self.nonce = str(regexp2.group(1))
        uri = "/au/logger/v1/public_config"
        resp = self.buildReq(uri, "GET", timestamp)

        if resp is None :
            return None

        timestamp = str(int(time.time()))
        regexp3 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp3 is not None) :
            self.nonce = str(regexp3.group(1))
        uri = "../v1/config"
        resp = self.buildReq(uri, "GET", timestamp)

        if resp is None :
            return None

        regexp4 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp4 is not None) :
            self.nonce = str(regexp4.group(1))
        

    def fetch(self, element) :
        if self.nonce is None :
            res = self.login()
            if res is None :
                return None

        timestamp = str(int(time.time()))
        uri = "/v1/feeds/ser"+self.ser+"?_="+timestamp
        resp = self.buildReq(uri, "GET", timestamp)
        try: 
            payload = json.loads(resp['html'])
            if payload is not None :
                measure = payload['feeds']['ser'+self.ser]['datastreams'][element]['data'][0]
                ts = measure['timestamp']
                ts_format = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
                measure['ts'] = int(time.mktime(ts_format.timetuple())) 
                return measure
        except ValueError as e:
            print("JSON error: "+resp['html'])
        return None

def main ():
    abb = APABB("192.168.1.154", "admin", "db6e106cf2b982d8dce1cf2ba2e0d449", "4:120399-3G96-3016")
    while True :
        m = abb.fetch('m101_1_PhVphA')
        if m is not None :
            abb.log_emoncms(m['ts'], 101, 'ABB_VOLTAGE_OUT', m['value'])
            m = abb.fetch('m101_1_W')
            abb.log_emoncms(m['ts'], 101, 'ABB_POWER_SOLAR_OUT', 1000*m['value'])
            m = abb.fetch('m101_1_TmpCab')
            abb.log_emoncms(m['ts'], 101, 'ABB_TEMP_INVERTER', m['value'])
            m = abb.fetch('m101_1_A')
            abb.log_emoncms(m['ts'], 101, 'ABB_CURRENT_SOLAR_OUT', m['value'])
            time.sleep(60)
        else :
            print("Unable to reach the inverter...")
            time.sleep(1200)

if __name__ == "__main__":
    main()
