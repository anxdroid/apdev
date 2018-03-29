import time
import urllib2
import json
import datetime
import calendar

class Termostato:
    APIKEY = "a7441c2c34fc80b6667fdb1717d1606f"
    urlCurrTemp = "http://192.168.1.12/emoncms/feed/timevalue.json"
    urlHeaters = "http://192.168.1.12/temp/jobs.php"
    #urlThresholds = "http://192.168.1.12/temp/thresholds.php?sensor=TEMP_DISIMPEGNO"
    urlThresholds = "http://192.168.1.12/temp/thresholds.php"

    sensor = "TEMP_SALOTTO"
    heatersMgrUsr = "anto"
    heatersMgrPwd = "resistore"
    minTemp = 17
    maxTemp = 20
    interval = 60

    def __init__(self, minTemp, maxTemp, interval):
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.interval = interval

    def startTermo(self) :
        while True:
            thresholds = self.getThresholds()
            self.minTemp = float(thresholds["min"])
            self.maxTemp = float(thresholds["max"])
            temp = self.getCurrTemp()
            #print str(temp)
            now = time.time()
            tempVal = float(temp["value"])
            tempTime = int(temp["time"])
            diffTempTime = now - tempTime
            status = self.getHeatersStatus()
            cmd = status["cmd"]
            cmdStatus = int(status["status"])
            cmdEnded = status["ended"]
            if cmdEnded is not None:
                date = datetime.datetime.strptime(cmdEnded, "%Y-%m-%d %H:%M:%S")
                #cmdTime = calendar.timegm(date.utctimetuple())
                cmdTime = time.mktime(date.timetuple())
                diffCmdTime = now - cmdTime
                print str(time.time())+": Temp "+str(diffTempTime)+" secs ago was "+str(tempVal)+" ("+str(self.minTemp)+"-"+str(self.maxTemp)+")"
                print str(time.time())+": Heaters "+str(diffCmdTime)+" secs ago where "+str(cmd)+" ("+str(cmdStatus)+")"
            if cmdEnded is None or diffTempTime > 120 :
                print "No decision taken !"
            else:
                if ((tempVal < self.minTemp) and (cmd != "HEATERS:ON" or cmdStatus != 2)) :
                    print "Start heaters !"
                    self.toggleHeatersStatus("HEATERS:ON")
                if ((tempVal > self.maxTemp) and (cmd != "HEATERS:OFF" or cmdStatus != 2)) :
                    print "Stop heaters !"
                    self.toggleHeatersStatus("HEATERS:OFF")
            
            time.sleep(self.interval)

    def getCurrTemp(self):
        url = self.urlCurrTemp+"?id=12&apikey="+self.APIKEY
        #print url
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        return data
    
    def toggleHeatersStatus(self, switch):
        url = self.urlHeaters+"?cmd="+switch
        print url
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.heatersMgrUsr, self.heatersMgrPwd)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        #opener.open(url)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        return data["data"][0]

    def getHeatersStatus(self):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.urlHeaters, self.heatersMgrUsr, self.heatersMgrPwd)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        #opener.open(self.urlHeaters)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(self.urlHeaters)
        data = json.loads(response.read())
        return data["data"][0]
    
    def getThresholds(self):
        urlToCall = self.urlThresholds+"?sensor="+self.sensor
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, urlToCall, self.heatersMgrUsr, self.heatersMgrPwd)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        #opener.open(self.urlThresholds)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(urlToCall)
        data = json.loads(response.read())
        return data["data"][0]

def main():
    termo = Termostato(18, 24, 10)
    #print str(termo.getThresholds())
    #status = termo.getHeatersStatus()
    #temp = termo.getCurrTemp()
    #termo.toggleHeatersStatus("ON")
    #termo.toggleHeatersStatus("OFF")
    termo.startTermo()


if __name__ == "__main__": main()
