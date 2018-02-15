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

    debug = False

    def log_emoncms(self, timestamp, nodeid, key, value):
        print(timestamp+" "+nodeid+" "+key+" "+value)
        conn = httplib.HTTPConnection(self.domain)
        url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+nodeid+"&json={"+key+":"+value+"}"
        #print url
        try:
            conn.request("GET", url)
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

        conn.request(method=method, url=path, headers=headers)
        resp = conn.getresponse()
        html = resp.read()
        headers = str(resp.msg)
        conn.close()
        return {'html':html, 'headers':headers}

    def __init__(self, host, username, password) :
        self.host = host
        self.username = username
        self.HA1 = password

    def login(self) :
        timestamp = str(int(time.time()))
        uri = "/v3/#/login"
        resp = self.buildReq(uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        uri = "../v1/status?_="+timestamp
        resp = self.buildReq(uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp1 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp1 is not None) :
            self.nonce = str(regexp1.group(1))
        resp = self.buildReq(uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp2 is not None) :
            self.nonce = str(regexp2.group(1))
        uri = "/au/logger/v1/public_config"
        resp = self.buildReq(uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp3 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp3 is not None) :
            self.nonce = str(regexp3.group(1))
        uri = "../v1/config"
        resp = self.buildReq(uri, "GET", timestamp)
        regexp4 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp4 is not None) :
            self.nonce = str(regexp4.group(1))

    def fetch(self, element, key) :
        if self.nonce is None :
            self.login()
        timestamp = str(int(time.time()))
        uri = "/v1/feeds/ser4:120399-3G96-3016?_="+timestamp
        resp = self.buildReq(uri, "GET", timestamp)
        try: 
            payload = json.loads(resp['html'])
            if payload is not None :
                measure = payload['feeds']['ser4:120399-3G96-3016']['datastreams'][element]['data'][0]
                #measure['ts'] = time.mktime(datetime.datetime.strptime(measure['timestamp'], "%Y-%m-%dT%H:%M:%S%").timetuple())
                
                return measure
        except ValueError as e:
            print("JSON error: "+resp['html'])

def main ():
    abb = APABB("192.168.1.18", "admin", "db6e106cf2b982d8dce1cf2ba2e0d449")
    voltage = abb.fetch('m101_1_PhVphA', 'ABB_VOLTAGE_OUT');
    print voltage

if __name__ == "__main__":
    main()
