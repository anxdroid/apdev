import multiprocessing
import socket
import os
import json
import RPi.GPIO as GPIO
import sqlite3
import time
from passlib.hash import apr_md5_crypt
import re

AUTH_TOKEN = "f_Yhkoljlj43_."
dbname = '/media/LaCie/Anto/templog.db'
values = {}


def doquery(category, key, value, source, notes):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO events (id, category, key, value, source, params) values (NULL, (?), (?), (?), (?), (?))", (category, key,value,source,notes))
    conn.commit()
    conn.close()

def check_threshold(id):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("thresholds")
    conn=sqlite3.connect(dbname)
    try:
        curs=conn.cursor()
        #logging.info("Querying...")
        curs.execute("SELECT * FROM thresholds WHERE active = 1 AND id = ?", (id, ))
	row = curs.fetchone()
	#print row
	#TODO: non tutti i sources sono dati acquisiti es. l'orario o (per ora) il fatto che la caldaia sia accesa
	curs.execute("SELECT source, value, timestamp FROM sensors WHERE source = (?) AND cast( ( strftime('%s',datetime('now'))-strftime('%s',timestamp) ) AS real ) < 60 ORDER BY timestamp DESC", (row[1], ))
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
        #logger.debug("Closing thresholds process")
        conn.close()

def triggers():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-triggers")
    logger.debug("Starting triggers process")
    conn=sqlite3.connect(dbname)
    try:
	while (True):
	        curs=conn.cursor()
        	#logging.info("Querying...")
	        for row in curs.execute("SELECT * FROM triggers WHERE active = 1 AND (last_result = 0 OR last_result IS NULL OR last_triggered IS NULL OR cast( ( strftime('%s',datetime('now'))-strftime('%s',last_triggered) ) AS real ) > 60)"):
        	    #print row
	            trigger = str(row[1])
                    cmd = str(row[2])
	            p = re.compile('\d+')
	            ids = p.findall(trigger)
	            #print trigger+" "+cmd
	            for id in ids:
	                check = check_threshold(id)
	                trigger = trigger.replace(str(id), str(check))
	                #print check
	            check = eval(trigger)
                    curs1 = conn.cursor()
	            if (check) :
			# do CMD
			print trigger+" ok => execute "+cmd
			curs1.execute("UPDATE triggers SET last_triggered = datetime('now'), last_result = 1 WHERE id = ?", (row[0], ))
	            	cmd_info = cmd.split(":")
			#doquery('TRGSRV', cmd_info[0], cmd_info[1], '127.0.0.1', "Trigger id: "+str(row[0]))
                    elif(row[5] == 1) :
			curs1.execute("UPDATE triggers SET last_triggered = datetime('now'), last_result = 0 WHERE id = ?", (row[0], ))
            
                    #print(check)
                    #logger.debug("Done trigger id %d", row[0])
                    conn.commit()
                    if (check):
			doquery('TRGSRV', cmd_info[0], cmd_info[1], '127.0.0.1', "Trigger id: "+str(row[0]))
		time.sleep(2)
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing triggers process")
        conn.close()

def jobs():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-jobs")
    logger.debug("Starting jobs process")
    conn=sqlite3.connect(dbname)
    AUTH = True
    try:
        while True:
            curs=conn.cursor()
            curs.execute("SELECT * FROM jobs WHERE status = 0 ORDER BY timestamp DESC")
            row = curs.fetchone()
            if row != None:
                curs.execute("UPDATE jobs SET status = 1, started = datetime('now') WHERE id = ?", (row[0],))
                conn.commit()
                logger.debug("Found job id %d", row[0])
                print row
                params = {}
                params["clientaddr"] = row[4]
                params["job_id"] = row[0]
                params = execute_cmd("JOBSRV", row[2], params, AUTH)
                AUTH = params["AUTH"]
                curs.execute("UPDATE jobs SET status = 2, ended = datetime('now') WHERE id = ?", (row[0],))
                conn.commit()
                logger.debug("Done job id %d", row[0])
            time.sleep(2)
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing jobs process")
        conn.close()
    

def deinit():
    GPIO.cleanup()

    conn=sqlite3.connect(dbname)
    key="STOP"
    value=str(os.getpid())
    source = socket.gethostbyname(socket.gethostname())
    params = {}
    params["pid"] = str(os.getpid())    
    doquery("SRV", key, value, source, json.dumps(params))

def init():
    conn=sqlite3.connect(dbname)
    key="START"
    value=str(os.getpid())
    source = socket.gethostbyname(socket.gethostname())
    params = {}
    params["pid"] = str(os.getpid()) 
    doquery("SRV", key, value, source, json.dumps(params))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)

def LED(arg, logger):
    args = arg.split("#")
    if args[0] == "1":
        GPIO.output(27, GPIO.HIGH)
        return "GPIO 27 HIGH"
    elif args[0] == "0":
        GPIO.output(27, GPIO.LOW)
        return "GPIO 27 LOW"
    elif args[0] == "R":
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.OUT)
        return "GPIO RESET"
    else:
        logger.debug("Error !")
        return "Error"

def doAUTH(user, password, logger):
    conn=sqlite3.connect(dbname)
    AUTH = False;
    try:
        curs=conn.cursor()
        #curs.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, password,))
        curs.execute("SELECT password FROM users WHERE username = ?", (user,))
	row = curs.fetchone()
        if row != None:
            #AUTH = True
		AUTH = apr_md5_crypt.verify(password, row[0])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing auth process")
        conn.close()
        return AUTH
    return AUTH


def RELAY(arg, logger):
    args = arg.split("#")
    if args[0] == "1":
        GPIO.output(18, GPIO.HIGH)
        return "GPIO 18 HIGH"
    elif args[0] == "0":
        GPIO.output(18, GPIO.LOW)
        return "GPIO 18 LOW"
    elif args[0] == "R":
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        return "GPIO RESET"
    else:
        logger.debug("Error !")
        return "Error"

def execute_cmd(category, data, params, AUTH):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-cmd")

    data_info = data.split(":")
    retval = data
    if len(data_info) > 1 :

        #conn=sqlite3.connect(dbname)
        #curs=conn.cursor()
        key=data_info[0]
        value=data_info[1]

        
        if AUTH == False and data_info[0] == "AUTH" :
            AUTH = doAUTH(data_info[1], data_info[2], logger)
            value = data_info[1]

        #if AUTH == False and data_info[0] == "AUTH" and data_info[1] == AUTH_TOKEN:
        #    AUTH = True
        #    value="****"
        
        if AUTH == False:
            logger.debug("Failed auth !")
            retval = "Get out !"
        elif data_info[0] != "AUTH" :
            if (data_info[0] == "RELAY"):
                retval = RELAY(data_info[1], logger)
            elif (data_info[0] == "LED"):
                retval = LED(data_info[1], logger)
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
        doquery(category, key, value, source, json.dumps(params))
    return params


def handle(connection, address):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    AUTH = False
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)

            params = {}
            params["clientaddr"] = address
            params = execute_cmd("CMDSRV", data, params, AUTH)
            AUTH = params["AUTH"]
            connection.sendall(params["retval"])
            logger.debug("Sent data %r", params["retval"])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

class Server(object):
    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self):
        process_jobs = multiprocessing.Process(target=jobs, args=())
        process_jobs.daemon = True
        process_jobs.start()


	values['TEMP_SALOTTO'] = 16.5
	values['TEMP_ESTERNA'] = 5
        values['HOURS'] = 18
	
	process_triggers = multiprocessing.Process(target=triggers, args=())
        process_triggers.daemon = True
        #process_triggers.start()
	
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            
            key="CONNECTION"
            value=str(process)
            source = socket.gethostbyname(socket.gethostname())
            params = {}
            params["clientaddr"] = address
            params["pid"] = str(os.getpid()) 
            params["thread"] = str(process)
            doquery("CMDSRV", key, value, source, json.dumps(params))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 82)
    try:
        init()
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
        deinit()
    logging.info("All done")
