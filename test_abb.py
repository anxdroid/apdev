import httplib, urllib
import re
import time
import hashlib
import json


class APABB(object):
    nodeids = {"101":{"ABB_POWER_SOLAR_OUT":"W", "ABB_CURRENT_SOLAR_OUT":"A", "ABB_VOLTAGE_OUT":"V", "ABB_TEMP_INVERTER":"&deg;"}}
    domain = "192.168.1.12"
    emoncmspath = "emoncms"
    apikey = "2a4e7605bb826a82ef3a54f4ff0267ed"

    nonce = None
    challenge = None
    username = "admin"
    # Hash of admin password
    HA1 = 'db6e106cf2b982d8dce1cf2ba2e0d449'
    nc = "00000002"
    cnonce = "ddf4bfcaf87acba9"
    qop = "auth"
    HA2 = None
    response = None

    def log_emoncms(self, timestamp, nodeid, key, value):
        print(timestamp+" "+nodeid+" "+key+" "+value)
        conn = httplib.HTTPConnection(self.domain)
        url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+nodeid+"&json={"+key+":"+value+"}"
        #print url
        try:
            conn.request("GET", url)
        except Exception as e:
            print "HTTP error: %s" % str(e)

    def buildReq(self, host, path, method, timestamp) :
        conn = httplib.HTTPConnection(host)
        conn.set_debuglevel(2)
        headers = {}

        if self.nonce is not None
            print "Nonce ------------------------------"
            print self.nonce
            print "------------------------------------"
            self.challenge = 'X-Digest realm="registered_user@power-one.com", nonce="'+self.nonce+'", qop="auth"'
            print "Challenge --------------------------"
            print self.challenge
            print "------------------------------------"

            HA2_md5 = hashlib.md5()
            HA2_md5.update(method+":"+uri)
            self.HA2 = HA2_md5.hexdigest();
            
            print "HA2 --------------------------------"
            print self.HA2
            print "------------------------------------"
            
            response_md5 = hashlib.md5()
            response_md5.update(HA1+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+HA2)
            self.response = response_md5.hexdigest();
            print "Response ---------------------------"
            print self.response
            print "------------------------------------"
            headers = {
                "Cookie": "filter=all; _ga=GA1.3.1163095045."+timestamp+"; _gid=GA1.3.915588772."+timestamp+"; _gat=1",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "it-IT,it;q=0.9,en;q=0.8,es;q=0.7",
                "Authorization": "X-Digest username=\""+self.username+"\", realm=\"registered_user@power-one.com\", nonce=\""+self.nonce+"\", uri=\""+uri+"\", response=\""+self.response+"\", qop="+self.qop+", nc="+nc+", cnonce=\""+self.cnonce+"\""}

        conn.request(method=method, url=path, headers=headers)
        resp = conn.getresponse()
        html = resp.read()
        headers = str(resp.msg)
        conn.close()
        return {'html':html, 'headers':headers}

    def login(self) :
        timestamp = str(int(time.time()))
        host = "192.168.1.18"
        uri = "/v3/#/login"
        resp = self.buildReq(host, uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        uri = "../v1/status?_="+timestamp
        resp = self.buildReq(host, uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp1 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp1 is not None) :
            self.nonce = str(regexp1.group(1))
        resp = self.buildReq(host, uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp2 is not None) :
            self.nonce = str(regexp2.group(1))
        uri = "/au/logger/v1/public_config"
        resp = buildReq(host, uri, "GET", timestamp)

        timestamp = str(int(time.time()))
        regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp3 is not None) :
            self.nonce = str(regexp3.group(1))
        uri = "../v1/config"
        resp = buildReq(host, uri, "GET", timestamp)
        regexp = re.search("nonce=\"([^\"]+)\"", resp['headers'])
        if (regexp is not None) :
            self.nonce = str(regexp2.group(1))

    def fetch(self, element, key) :
        self.login()
        timestamp = str(int(time.time()))
        uri = "/v1/feeds/ser4:120399-3G96-3016?_="+timestamp
        resp = buildReq(host, uri, "GET", timestamp)
        payload = json.loads(resp['html'])
        #m101_1_PhVphA = payload['feeds']['ser4:120399-3G96-3016']['datastreams']['m101_1_PhVphA']
        measure = payload['feeds']['ser4:120399-3G96-3016']['datastreams'][element]
        #for measure in m101_1_PhVphA['data'] :
        #    print measure
        self.log_emoncms(timestamp, 101, key, measure['value'])


def main ():
    abb = APABB()
    abb.fetch('m101_1_PhVphA', 'ABB_VOLTAGE_OUT');
