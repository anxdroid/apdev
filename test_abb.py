import httplib, urllib
import re
import time
import hashlib
import json


class AP_ABB(object):
    nodeids = {"101":{"ABB_POWER_SOLAR":"W", "ABB_CURRENT_SOLAR":"A", "ABB_VOLTAGE":"V", "ABB_TEMP_INVERTER":"&deg;"}}
    domain = "192.168.1.12"
    emoncmspath = "emoncms"
    apikey = "2a4e7605bb826a82ef3a54f4ff0267ed"


    def log_emoncms(self, timestamp, nodeid, key, value):
        print(timestamp+" "+nodeid+" "+key+" "+value)
        conn = httplib.HTTPConnection(self.domain)
        url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+nodeid+"&json={"+key+":"+value+"}"
        #print url
        conn.request("GET", url)

def buildReq(host, path, method, timestamp, nonce=None) :
    conn = httplib.HTTPConnection(host)
    conn.set_debuglevel(2)
    headers = {}

    if nonce is not None :
        print "Nonce ------------------------------"
        print nonce
        print "------------------------------------"
        challenge = 'X-Digest realm="registered_user@power-one.com", nonce="'+nonce+'", qop="auth"'
        print "Challenge --------------------------"
        print challenge
        print "------------------------------------"

        HA1 = 'db6e106cf2b982d8dce1cf2ba2e0d449'
        HA2_md5 = hashlib.md5()
        HA2_md5.update("GET:"+uri)
        HA2 = HA2_md5.hexdigest();
        print "HA2 --------------------------------"
        print HA2
        print "------------------------------------"
        username = "admin"
        nc = "00000002"
        cnonce = "ddf4bfcaf87acba9"
        qop = "auth"
        response_md5 = hashlib.md5()
        response_md5.update(HA1+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+HA2)
        response = response_md5.hexdigest();
        print "Response ---------------------------"
        print response
        print "------------------------------------"
        headers = {
            "Cookie": "filter=all; _ga=GA1.3.1163095045."+timestamp+"; _gid=GA1.3.915588772."+timestamp+"; _gat=1",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8,es;q=0.7",
            "Authorization": "X-Digest username=\""+username+"\", realm=\"registered_user@power-one.com\", nonce=\""+nonce+"\", uri=\""+uri+"\", response=\""+response+"\", qop="+qop+", nc="+nc+", cnonce=\""+cnonce+"\""}

    conn.request(method=method, url=path, headers=headers)
    resp = conn.getresponse()
    html = resp.read()
    headers = str(resp.msg)
    conn.close()
    return {'html':html, 'headers':headers}

timestamp = str(int(time.time()))
host = "192.168.1.18"
uri = "/v3/#/login"
resp = buildReq(host, uri, "GET", timestamp)

timestamp = str(int(time.time()))
uri = "../v1/status?_="+timestamp
resp = buildReq(host, uri, "GET", timestamp)
print resp['headers']

timestamp = str(int(time.time()))
regexp1 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
nonce = str(regexp1.group(1))
resp = buildReq(host, uri, "GET", timestamp, nonce)
#print resp['headers']

timestamp = str(int(time.time()))
regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
if (regexp2 is not None) :
    nonce = str(regexp2.group(1))
uri = "/au/logger/v1/public_config"
resp = buildReq(host, uri, "GET", timestamp, nonce)
print resp['headers']


timestamp = str(int(time.time()))
regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
if (regexp2 is not None) :
    nonce = str(regexp2.group(1))
uri = "../v1/config"
resp = buildReq(host, uri, "GET", timestamp, nonce)
print resp['headers']

timestamp = str(int(time.time()))
regexp2 = re.search("nonce=\"([^\"]+)\"", resp['headers'])
if (regexp2 is not None) :
    nonce = str(regexp2.group(1))
uri = "/v1/feeds/ser4:120399-3G96-3016?_="+timestamp
resp = buildReq(host, uri, "GET", timestamp, nonce)
#print resp['html']
payload = json.loads(resp['html'])
m101_1_PhVphA = payload['feeds']['ser4:120399-3G96-3016']['datastreams']['m101_1_PhVphA']
#for measure in m101_1_PhVphA['data'] :
#    print measure
log_emoncms(timestamp, 101, apikey, 
