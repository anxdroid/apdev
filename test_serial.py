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
        self.dbconn.ping(True)
	print self.dbconn

        key="START"
        self.srvaddress = socket.gethostbyname(socket.gethostname())
        self.srvpid = os.getpid()
        params = {}
        value = params["pid"] = str(self.srvpid)
        self.log_event("SRV", key, value, self.srvaddress, json.dumps(params))

    def __init__(self):
            self.srvinit()

    def log_measurement(self, timestamp, value, sensor, unit):
        curs = self.dbconn.cursor()
        sql = "INSERT INTO sensors (timestamp, value, sensor, source, unit) values(%s, %s, %s, %s, %s)"
        try:
            curs.execute(sql, (timestamp, value, sensor, self.srvaddress, unit))
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

    def serialread(self, path):
        myline = ""
        try:
            if(self.ser.isOpen() == False):
            	self.ser.open()
            #inbuff = self.ser.inWaiting()
            if (self.ser.inWaiting() > 0):
                myline = self.ser.readline()
                #self.ser.flushInput()
	except IOError as e:
            #Disconnect of USB->UART occured
            #self.ser.flushInput()
            print(e)
            self.ser.close()
            #time.sleep(10)
            return -1
        except TypeError as e:
            #Disconnect of USB->UART occured
            #self.ser.flushInput()
            print(e)
            self.ser.close()
            time.sleeps(10)
        except serial.SerialException as e:
            #There is no new data from serial port
            #self.ser.flushInput()
            print(e)
            self.ser.close()
            time.sleep(10)
        else:
            #Some data was received
            p = re.compile('[^:\s]+:[\d|\.|-]+:[^\s]+')
            vals = p.findall(myline)
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print myline
            if (len(vals) > 0):
                for val in vals:
                    info = val.split(':')
                    if (len(info) == 3 and info[0] != 'MILLIS'):
                        print timestamp+" "+str(val)
                        self.log_measurement(timestamp, info[1], info[0], info[2])
        #self.ser.flushInput()
	return 0

    def serialsrv(self):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("process-serial")
        logger.debug("Starting serial process")
        path = '/dev/ttyACM0'
	try:
            os.stat(path)
	except OSError:
            path = '/dev/ttyACM1'
        try:
            self.ser = serial.Serial(path,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                xonxoff=0,
                rtscts=0
            )
            self.ser.setDTR(False)
            self.ser.flushInput()
            time.sleep(3)
            self.ser.setDTR(True)
        except IOError as e:
            print(e)
            
        #time.sleep(1)

        try:
            while True: 
                ret = self.serialread(path)
		if ret == -1 :
			if path == '/dev/ttyACM1' :
				path = '/dev/ttyACM0'
			else :
				path = '/dev/ttyACM1'
		        try :
				self.ser = serial.Serial(path,
		        	        baudrate=9600,
	        		        bytesize=serial.EIGHTBITS,
        	        		parity=serial.PARITY_NONE,
			                stopbits=serial.STOPBITS_ONE,
		        	        timeout=1,
		                	xonxoff=0,
			                rtscts=0
				)
                                self.ser.setDTR(False)
                                self.ser.flushInput()
				time.sleep(3)
				self.ser.setDTR(True)
		        except IOError as e:
		            print(e)
		            time.sleep(2)
        except:
            logger.exception("Problem handling request")
        finally:
            logger.debug("Closing serial process")

    def start(self):
        #process_serials = multiprocessing.Process(target=self.serialsrv, args=())
        #process_serials.daemon = True
        #process_serials.start()
        self.serialsrv()


def main ():
    server = APServer()
    server.start()

if __name__ == "__main__":
        main()
