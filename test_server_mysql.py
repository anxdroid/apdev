import logging
import multiprocessing
import socket
import os
import json
import RPi.GPIO as GPIO
import time
from passlib.hash import apr_md5_crypt
import re
import MySQLdb
import datetime
import sys
import Adafruit_DHT

class APServer(object):
		def srvinit(self):
				self.dbconn = MySQLdb.connect('localhost', 'apdb', 'pwd4apdb', 'apdb')
				self.dbconn.autocommit(True)
				print self.dbconn

				key="START"
				self.srvaddress = socket.gethostbyname(socket.gethostname())
				self.srvpid = os.getpid()
				params = {}
				value = params["pid"] = str(self.srvpid)
				self.log_event("SRV", key, value, self.srvaddress, json.dumps(params))
				#self.dbconn.commit()

				GPIO.setmode(GPIO.BCM)
				GPIO.setup(18, GPIO.OUT)
				GPIO.setup(27, GPIO.OUT)
				GPIO.output(18, GPIO.HIGH)

				

		def __init__(self, hostname, port):
				self.logger = logging.getLogger("apserver")
				self.hostname = hostname
				self.port = port
				self.srvinit()


		def srvdeinit(self):
				GPIO.cleanup()
				self.socket.shutdown(socket.SHUT_RDWR)
				self.socket.close()
				key="STOP"
				params = {}
				value = params["pid"] = str(self.srvpid)
				self.log_event("SRV", key, value, self.srvaddress, json.dumps(params))
				#self.dbconn.commit()
				self.dbconn.close()

		def __del__(self):
				self.srvdeinit()

		def log_measurement(self, value, source, unit):
			curs = self.dbconn.cursor()
			sql = "INSERT INTO sensors (value, source, unit) values(%s, %s, %s)"
			try:
				curs.execute(sql, (value,source,unit))
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

		def do_AUTH(self, user, password, logger):
			AUTH = False;
			try:
				curs = self.dbconn.cursor()
				sql = "SELECT password FROM users WHERE username = %s"
				curs.execute(sql, (user,))
				print curs._last_executed
				row = curs.fetchone()
				if row != None:
						AUTH = apr_md5_crypt.verify(password, row[0])

			except MySQLdb.Error, e:
				try:
					print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				except IndexError:
					print "MySQL Error: %s" % str(e)
			finally:
				logger.debug("Closing auth process")

			return AUTH

		def HEATERS(self, arg, logger):
			args = arg.split("#")
			if args[0] == "OFF" or args[0] == "1":
				GPIO.output(18, GPIO.HIGH)
				return "GPIO 18 HIGH"
			elif args[0] == "ON" or args[0] == "0":
				GPIO.output(18, GPIO.LOW)
				return "GPIO 18 LOW"
			elif args[0] == "RESET":
				GPIO.cleanup()
				GPIO.setmode(GPIO.BCM)
				GPIO.setup(18, GPIO.OUT)
				return "GPIO RESET"
			else:
				logger.debug("Error !")
				return "Error"
						
		def execute_cmd(self, category, data, params, AUTH):
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("process-cmd")

			data_info = data.split(":")
			retval = data
			if len(data_info) > 1 :
				key=data_info[0]
				value=data_info[1]

				
				if AUTH == False and data_info[0] == "AUTH" and len(data_info) == 3:
					AUTH = self.do_AUTH(data_info[1], data_info[2], logger)
					value = data_info[1]
				
				if AUTH == False:
					logger.debug("Failed auth !")
					retval = "Get out !"
				elif data_info[0] != "AUTH" :
					if (data_info[0] == "HEATERS" or data_info[0] == "RELAY"):
						retval = self.HEATERS(data_info[1], logger)
					#elif (data_info[0] == "LED"):
					#	retval = LED(data_info[1], logger)
					else :
						logger.debug("Unknown command !")
						retval = "Unknown command !"
				else:
					logger.debug("Authenticated !")
					retval = "Welcome !"
			else:
				key = data
				val = "ERR"
				retval = "Params error"

			params["retval"] = retval
			params["AUTH"] = AUTH
			if data_info[0] == "AUTH" or AUTH:
				source = socket.gethostbyname(socket.gethostname())
				self.log_event(category, key, value, source, json.dumps(params))
				#self.dbconn.commit()
			return params

		def check_threshold(self, id):
			import logging
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("thresholds")
			try:
				curs = self.dbconn.cursor()
				#logging.info("Querying...")
				sql = "SELECT * FROM thresholds WHERE active = 1 AND id = %s"
				curs.execute(sql, (id, ))
				row = curs.fetchone()
				#print row
				#TODO: non tutti i sources sono dati acquisiti es. l'orario o (per ora) il fatto che la caldaia sia accesa
				if (row != None) :
					sql = "SELECT source, value, timestamp FROM sensors WHERE source = %s AND TIMESTAMPDIFF(SECOND, timestamp, NOW()) < 60 ORDER BY timestamp DESC"
					curs.execute(sql, (row[1], ))
					row1 = curs.fetchone()
					#print row1
					if (row1 != None) :
						print id+": "+row[1]+" = "+str(row1[1])+" ["+str(row[2])+","+str(row[3])+"]"
						if (row1[1] >= row[2] and row1[1] <= row[3]):
							return True
					return False
					#logger.debug("Done threshold id %d", row[0])
			except:
				logger.exception("Problem handling request")
			finally:
				logger.debug("Closing thresholds process")

		def sensorsrv(self):
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("process-sensors")
			logger.debug("Starting sensors process")
			try:
				while (True) :
					tfile = open("/sys/bus/w1/devices/28-000003fa0104/w1_slave")
					text = tfile.read()
					tfile.close()
					secondline = text.split("\n")[1]
					temperaturedata = secondline.split(" ")[9]
					temperature = float(temperaturedata[2:])
					temperature = temperature / 1000
					self.log_measurement(temperature, "TEMP_SALOTTO", "&deg;")
					
					# Humidity

					humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
					if humidity is not None and temperature is not None:
						#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
						if (temperature > 0 and temperature < 50):
								self.log_measurement(temperature, "TEMP_DISIMPEGNO", "&deg;")
						if (humidity > 0 and humidity <= 100):
								self.log_measurement(humidity, "UMID_DISIMPEGNO", "%")
								
					time.sleep(30)
			except:
				logger.exception("Problem handling request")
			finally:
				logger.debug("Closing sensors process")
		
				
		def triggersrv(self):
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("process-triggers")
			logger.debug("Starting triggers process")
			try:
				while (True):
					#logger.debug("Searching for triggers...")
					curs = self.dbconn.cursor()
					sql = "SELECT * FROM triggers WHERE active = 1 AND (last_result = 0 OR last_result IS NULL OR last_triggered IS NULL OR TIMESTAMPDIFF(SECOND, last_triggered, NOW()) > 60)"
					curs.execute(sql)
					rows = curs.fetchall()
					for row in rows:
						#print row
						trigger = str(row[1])
						cmd = str(row[2])
						p = re.compile('\d+')
						ids = p.findall(trigger)
						#print trigger+" "+cmd
						for id in ids:
							check = self.check_threshold(id)
							trigger = trigger.replace(str(id), str(check))
							#print check
						check = eval(trigger)
						
						if (check or row[5] == 1):
							sql = "UPDATE triggers SET last_triggered = NOW(), last_result = %s WHERE id = %s"
							res = 0;
							if (check) :
								# do CMD
								print trigger+" ok => execute "+cmd
								res = 1
							#elif(row[5] == 1) :
							#	res = 0
							curs.execute(sql, (res, row[0], ))
							#self.dbconn.commit()
							
						logger.debug("Done trigger id %d", row[0])
						
						if (check):
							#cmd_info = cmd.split(":")
							#self.log_event('TRGSRV', cmd_info[0], cmd_info[1], '127.0.0.1', "Trigger id: "+str(row[0]))
							params = {}
							AUTH = True
							params["trigger_id"] = row[0]
							params = self.execute_cmd("TRIGGERSRV", cmd, params, AUTH)
					#curs.close()
					time.sleep(2)
			except:
				logger.exception("Problem handling request")
			finally:
				logger.debug("Closing triggers process")
			
		def jobsrv(self):
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("process-jobs")
			logger.debug("Starting jobs process")
			AUTH = True
			try:
				while True:
					curs = self.dbconn.cursor()
					#print curs
					sql = "SELECT * FROM jobs WHERE status = 0 ORDER BY timestamp DESC"
					#logger.debug("Searching for jobs...")
					curs.execute(sql)
					rows = curs.fetchall()
					for row in rows:
						row = rows[0]
						sql = "UPDATE jobs SET status = 1, started = NOW() WHERE id = %s"
						curs.execute(sql, (row[0],))
						#self.dbconn.commit()
						logger.debug("Found job id %d", row[0])
						params = {}
						params["clientaddr"] = row[4]
						params["job_id"] = row[0]
						params = self.execute_cmd("JOBSRV", row[2], params, AUTH)
						AUTH = params["AUTH"]
						sql = "UPDATE jobs SET status = 2, ended = NOW() WHERE id = %s"
						curs.execute(sql, (row[0],))
						#self.dbconn.commit()
						logger.debug("Done job id %d", row[0])
						break
					#curs.close()
					time.sleep(2)
			except:
				logger.exception("Problem handling request")
			finally:
				logger.debug("Closing jobs process")
			
		def cmdsrv(self, clientconn, address):
			logging.basicConfig(level=logging.DEBUG)
			logger = logging.getLogger("process-%r" % (address,))
			AUTH = False
			try:
				logger.debug("Connected %r at %r", clientconn, address)
				while True:
					data = clientconn.recv(1024)
					if data == "":
						logger.debug("Socket closed remotely")
						break
					logger.debug("Received data %r", data)

					params = {}
					params["clientaddr"] = address
					params = self.execute_cmd("CMDSRV", data, params, AUTH)
					AUTH = params["AUTH"]
					clientconn.sendall(params["retval"])
					logger.debug("Sent data %r", params["retval"])
			except:
				logger.exception("Problem handling request")
			finally:
				logger.debug("Closing socket")
				clientconn.close()



		def start(self):

				process_jobs = multiprocessing.Process(target=self.jobsrv, args=())
				process_jobs.daemon = True
				process_jobs.start()

				process_triggers = multiprocessing.Process(target=self.triggersrv, args=())
				process_triggers.daemon = True
				#process_triggers.start()
				
				process_sensors = multiprocessing.Process(target=self.sensorsrv, args=())
				process_sensors.daemon = True
				process_sensors.start()

				self.logger.debug("listening")
				self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				self.socket.bind((self.hostname, self.port))
				self.socket.listen(1)

				while True:
						clientconn, address = self.socket.accept()
						self.logger.debug("Got connection")
						process_client = multiprocessing.Process(target=self.cmdsrv, args=(clientconn, address))

						key="CONNECTION"
						value=str(process_client)
						source = socket.gethostbyname(socket.gethostname())
						params = {}
						params["clientaddr"] = address
						params["pid"] = str(os.getpid())
						params["thread"] = str(process_client)
						self.log_event("CMDSRV", key, value, source, json.dumps(params))
						#self.dbconn.commit()
						process_client.daemon = True
						process_client.start()
						self.logger.debug("Started process %r", process_client)

def main ():
	logging.basicConfig(level=logging.DEBUG)
	server = APServer("0.0.0.0", 82)

	try:
			logging.info("Listening")
			server.start()
	except:
			logging.exception("Unexpected exception")
	finally:
			logging.info("Shutting down")
			for process in multiprocessing.active_children():
					logging.info("Shutting down process %r", process)
					process.terminate()
					process.join()
	server.srvdeinit
	logging.info("All done")

if __name__ == "__main__":
	main()



