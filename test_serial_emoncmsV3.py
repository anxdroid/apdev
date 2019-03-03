import serial
#import MySQLdb
import time
import re
import datetime
import logging
import socket
import multiprocessing
import os
import sys
import json
import httplib
import urllib2
import json
import serial.tools.list_ports
import sys, traceback
from subprocess import Popen, PIPE
import fcntl

import BlynkLib
from BlynkTimer import BlynkTimer

USBDEVFS_RESET= 21780

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BlynkSerial(object):
# id nodo
#	10: ARDUINO_EMONTX
	nodeids = {
		"10":{"POWER_SOLAR":30, "CURRENT_SOLAR":31, "VOLTAGE":0, "TEMP_TERRAZZO":6},
	}

	authToken = "736662121c984b3da398b973b54a3bd3"
	port = 8080

	domain = "192.168.1.9"
	emoncmspath = "emoncms"
	apikey = "2a4e7605bb826a82ef3a54f4ff0267ed"
	urlJobs = "http://192.168.1.9/temp/jobs.php"
	jobsUsr = "anto"
	jobsPwd = "resistore"

	sendingCmd = False

	lastUSBreading = 0

	def resetSerial(self, driver):
		try:
			lsusb_out = Popen("lsusb | grep -i %s"%driver, shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, close_fds=True).stdout.read().strip().split()
			bus = lsusb_out[1]
			device = lsusb_out[3][:-1]
			f = open("/dev/bus/usb/%s/%s"%(bus, device), 'w', os.O_WRONLY)
			fcntl.ioctl(f, USBDEVFS_RESET, 0)
		except Exception, msg:
			print "failed to reset device:", msg	

	def initSerial(self):
		#print "Resetting ttyACM..."
		path = ""
		for port_no, description, address in serial.tools.list_ports.comports() :
			if 'ACM' in description:
				#print(address)
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

				if(self.serACM.isOpen() == False):
					self.serACM.open() 
				self.serACM.setDTR(False)
				self.serACM.flushInput()
				time.sleep(1)
				self.serACM.setDTR(True)
			except IOError as e:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				print "*** print_tb:"
				traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
				self.resetSerial("Arduino")
				self.initSerial()
		else:
			print("Serial not found !")
			time.sleep(2)
			self.initSerial()
		return path	

	def __init__(self, blynk):
		key="START"
		self.blynk = blynk
		print("Starting serial process")
		self.resetSerial("FT232")
		pathACM = self.initSerial()

	def log(self, nodeid, key, value) :
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print bcolors.BOLD+timestamp+bcolors.ENDC+": "+nodeid+" "+key+" "+bcolors.OKBLUE+value+bcolors.ENDC

	def logblynk(self, nodeid, key, value):
		try:
			print str(key)+" "+str(value)
			self.blynk.virtual_write(key, abs(float(value)))
		except Exception as e:
			print "Blynk error: %s" % str(e)

	def logemoncms(self, nodeid, key, value):
		conn = httplib.HTTPConnection(self.domain)
		url = "/"+self.emoncmspath+"/input/post.json?apikey="+self.apikey+"&node="+nodeid+"&json={"+key+":"+value+"}"
		try:
			conn.request("GET", url)
		except Exception as e:
			print "HTTP error: %s" % str(e)

	def parsereading(self, myline):
		#Some data was received
		p = re.compile('[^:\s]+:[^:\s]+:[\d|\.|-]+:[^\s]+')
		vals = p.findall(myline)
		if (len(vals) > 0):
			for val in vals:
				info = val.split(':')
				if (len(info) == 4 and info[0] != 'MILLIS'):
					if (info[0] in self.nodeids) :
						if (info[1] in self.nodeids[info[0]]) :
							self.logblynk(info[0], self.nodeids[info[0]][info[1]], info[2])
							self.logemoncms(info[0], info[1], info[2])
							self.log(info[0], info[1], info[2])
					else :
						ts = time.time()
						timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						print timestamp+" "+str(val)+" not ok !"	

	def serialReadACM(self):
		myline = ""
		try:
			if(self.serACM.isOpen() == False):
				self.serACM.open()
			start = time.time()
			msg = ""
			while (self.serACM.inWaiting() == 0):
				now = time.time()
				diff = 1000 * (now - start)
				tokens = str(diff).split(".")
				intdiff = int(tokens[0])
				if (intdiff % 1000 == 0 and intdiff > 0) :
					msg += tokens[0]+'...'
			if (self.serACM.inWaiting() > 0):
				myline = self.serACM.readline()
				if (myline != "" and myline != "\r" and myline != "\n" and len(msg) > 1) :
					print bcolors.WARNING+msg+bcolors.ENDC
					self.serACM.flushInput()
		except IOError as e:
			self.initSerial()
		except TypeError as e:
			print(e)
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print "*** print_tb:"
			traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
			self.serACM.flushInput()
			self.serACM.close()
			time.exc_type, exc_value, exc_traceback = sys.exc_info()
			print "*** print_tb:"
			time.sleep(2)
			self.initSerial()
			#time.exc_type, exc_value, exc_traceback = sys.exc_info()
			print "*** print_tb:"
			time.sleep(5)
		except serial.SerialException as e:
			print(e)
			print "Error on line "+format(sys.exc_info()[-1].tb_lineno)()
			self.serACM.flushInput()
			self.serACM.close()
			time.exc_type, exc_value, exc_traceback = sys.exc_info()
			print "*** print_tb:"
			time.sleep(2)
			self.initSerial()
		return myline		

	def serialRead(self):
		#try:
			myline = self.serialReadACM()
			if (myline != '') :
				self.parsereading(myline)
			sys.stdout.flush()
		#except:
		#	print("Problem handling request")
		#finally:
		#	print("Closing serial process")

authToken = "736662121c984b3da398b973b54a3bd3"
port = 8080
ip = "192.168.1.9"
blynk = BlynkLib.Blynk(authToken, server=ip, port=port)
timer = BlynkTimer()

@blynk.ON("connected")
def blynk_connected(ping):
	print('Blynk ready. Ping:', ping, 'ms')

@blynk.ON("disconnected")
def blynk_disconnected():
	print('Blynk disconnected')

@blynk.ON("V*")
def blynk_handle_vpins(pin, value):
	print("V{} value: {}".format(pin, value))

@blynk.ON("readV*")
def blynk_handle_vpins_read(pin):
	print("Server asks a value for V{}".format(pin))
	blynk.virtual_write(pin, 0)

def main():
	sys.stdout = open("/var/log/domotic.log", "w")
	blynkSerial = BlynkSerial(blynk)
	timer.set_interval(5, blynkSerial.serialRead)
	while True:
		blynk.run()
		timer.run()

if __name__ == "__main__":
		main()
