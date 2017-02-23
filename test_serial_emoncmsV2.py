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
import httplib
import serial.tools.list_ports

class APServer(object):
# id nodo
#	10: ARDUINO_EMONTX
	nodeids = {
		"10":{"POWER_SOLAR":"W", "CURRENT_SOLAR":"A", "VOLTAGE":"V", "TEMP_TERRAZZO":"&deg;"},
		"40":{"CURRENT_TERMO":"A"}
	}
	domain = "192.168.1.3"
	emoncmspath = "emoncms"
	apikey = "2a4e7605bb826a82ef3a54f4ff0267ed"

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

	def log_emoncms(self, timestamp, nodeid, key, value):
		print timestamp+" "+nodeid+" "+key+" "+value
		conn = httplib.HTTPConnection(self.domain)
		url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+nodeid+"&json={"+key+":"+value+"}"
		print url
		conn.request("GET", url)

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

	def parsereading(self, myline):
		#Some data was received
		p = re.compile('[^:\s]+:[^:\s]+:[\d|\.|-]+:[^\s]+')
		vals = p.findall(myline)
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print myline
		if (len(vals) > 0):
			for val in vals:
				info = val.split(':')
				if (len(info) == 4 and info[0] != 'MILLIS'):
					if (info[0] in self.nodeids and info[1] in self.nodeids[info[0]]) :
						print timestamp+" "+str(val)
						self.log_emoncms(timestamp, info[0], info[1], info[2])
					else :
						print timestamp+" "+str(val)+" not ok !"		

	def serialreadUSB(self, path):
		myline = ""
		try:
			if(self.serUSB.isOpen() == False):
				self.serUSB.open()
			if (self.serUSB.inWaiting() > 0):
				myline = self.serUSB.readline()
				self.serUSB.flushInput()
		except IOError as e:
			self.initserialUSB()
		except TypeError as e:
			print(e)
			self.serUSB.flushInput()
			self.serUSB.close()
			time.sleeps(5)
		except serial.SerialException as e:
			#There is no new data from serial port
			print(e)
			self.serUSB.flushInput()
			self.serUSB.close()
			time.sleep(5)
		else:
			self.parsereading(myline)
		return path


	def serialreadACM(self, path):
		myline = ""
		try:
			if(self.serACM.isOpen() == False):
				self.serACM.open()
			if (self.serACM.inWaiting() > 0):
				myline = self.serACM.readline()
				self.serACM.flushInput()
		except IOError as e:
			path = self.initserialACM()
		except TypeError as e:
			print(e)
			self.serACM.flushInput()
			self.serACM.close()
			time.sleeps(5)
		except serial.SerialException as e:
			#There is no new data from serial port
			print(e)
			self.serACM.flushInput()
			self.serACM.close()
			time.sleep(5)
		else:
			self.parsereading(myline)
		return path

	def initserialACM(self):
		path = ""
		for port_no, description, address in serial.tools.list_ports.comports() :
			if 'ACM' in description:
				print(address)
				path = port_no
				break
		if path != "" :
			print "Using "+path
			try:
				self.serACM = serial.Serial(path,
					baudrate=9600,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=1,
					xonxoff=0,
					rtscts=0
				)
				self.serACM.setDTR(False)
				self.serACM.flushInput()
				time.sleep(5)
				self.serACM.setDTR(True)
			except IOError as e:
				print(e)
		return path

	def initserialUSB(self):
		path = ""
		for port_no, description, address in serial.tools.list_ports.comports() :
			if 'USB' in description:
				print(address)
				path = port_no
				break

		if path != "" :
			print "Using "+path
			try:
				self.serUSB = serial.Serial(path,
					baudrate=9600,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=1,
					xonxoff=0,
					rtscts=0
				)
				self.serUSB.setDTR(False)
				self.serUSB.flushInput()
				time.sleep(5)
				self.serUSB.setDTR(True)
			except IOError as e:
				print(e)
		return path				

	def serialsrv(self):
		logging.basicConfig(level=logging.DEBUG)
		logger = logging.getLogger("process-serial")
		logger.debug("Starting serial process")

		pathACM = self.initserialACM()
		pathUSB = self.initserialUSB()
		try:
			while True: 
				pathACM = self.serialreadACM(pathACM)
				pathUSB = self.serialreadUSB(pathUSB)		
				time.sleep(3)
		except:
			logger.exception("Problem handling request")
		finally:
			logger.debug("Closing serial process")

	def start(self):
		#process_serials = multiprocessing.Process(target=self.serACMialsrv, args=())
		#process_serials.daemon = True
		#process_serials.start()
		self.serialsrv()


def main ():
	server = APServer()
	server.start()

if __name__ == "__main__":
		main()
