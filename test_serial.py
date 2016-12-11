import serial
import MySQLdb
import time
import re
import datetime
import logging
import socket
import multiprocessing
import os
import json

class APServer(object):
    def srvinit(self):
        self.dbconn = MySQLdb.connect('192.168.1.3', 'apdb', 'pwd4apdb', 'apdb')
        self.dbconn.autocommit(True)
        print self.dbconn

        key="START"
        self.srvaddress = socket.gethostbyname(socket.gethostname())
        self.srvpid = os.getpid()
        params = {}
        value = params["pid"] = str(self.srvpid)
        self.log_event("SRV", key, value, self.srvaddress, json.dumps(params))
        #self.ser = serial.Serial('/dev/ttyACM0', 9600)

        self.ser = serial.Serial('/dev/ttyS0',
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1,
                    xonxoff=0,
                    rtscts=0
                    )

# Toggle DTR to reset Arduino
        self.ser.setDTR(False)
        time.sleep(1)
# toss any data already received, see
# http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
        self.ser.flushInput()
        self.ser.setDTR(True)


    def __init__(self):
            self.srvinit()

    def log_measurement(self, timestamp, value, source, unit):
        curs = self.dbconn.cursor()
        sql = "INSERT INTO sensors (timestamp, value, source, unit) values(%s, %s, %s, %s)"
        try:
            curs.execute(sql, (timestamp, value,source,unit))
            #print curs._last_executed
            #print curs.lastrowid
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

    def log_event(self, category, key, value, source, notes):
            curs = self.dbconn.cursor()
            sql = "INSERT INTO events (category, `cmd`, value, source, params) values (%s, %s, %s, %s, %s)"
            #print sql
            try:
                curs.execute(sql, (category, key, value, source, notes,))
                #print curs._last_executed
                #print curs.lastrowid
            except MySQLdb.Error, e:
                try:
                    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                except IndexError:
                    print "MySQL Error: %s" % str(e)

    def serialsrv(self):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("process-serial")
        logger.debug("Starting serial process")
        try:
            while True:
                p = re.compile('[\d|\.|-]+')
                myline = self.ser.readline()
                vals = p.findall(myline)
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                if (len(vals) == 3):
                    print myline
                    for val in vals:
                        print st+" "+str(val)
                        #print ser.readline()
                time.sleep(2)
        except:
            logger.exception("Problem handling request")
        finally:
            logger.debug("Closing serial process")

    def start(self):
        process_serials = multiprocessing.Process(target=self.serialsrv, args=())
        process_serials.daemon = True
        process_serials.start()


def main ():
    server = APServer()
    server.start()

if __name__ == "__main__":
        main()
