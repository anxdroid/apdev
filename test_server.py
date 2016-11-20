import multiprocessing
import socket
import os
import json
import RPi.GPIO as GPIO
import sqlite3

AUTH_TOKEN = "f_Yhkoljlj43_."
dbname = '/media/LaCie/Anto/templog.db'

def doquery(key, value, source, notes):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO events (id, category, key, value, source, params) values(NULL, 'CMDSRV', (?), (?), (?), (?))", (key,value,source,notes))
    conn.commit()
    conn.close()

def deinit():
    GPIO.cleanup()

    conn=sqlite3.connect(dbname)
    key="STOP"
    value=str(os.getpid())
    source = socket.gethostbyname(socket.gethostname())
    params = {}
    params["pid"] = str(os.getpid())    
    doquery(key, value, source, json.dumps(params))

def init():
    conn=sqlite3.connect(dbname)
    key="START"
    value=str(os.getpid())
    source = socket.gethostbyname(socket.gethostname())
    params = {}
    params["pid"] = str(os.getpid()) 
    doquery(key, value, source, json.dumps(params))

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

            data_info = data.split(":")
            retval = data
            if len(data_info) > 1 :

                #conn=sqlite3.connect(dbname)
                #curs=conn.cursor()
                key=data_info[0]
                value=data_info[1]
                params = {}
                params["clientaddr"] = address 

                if AUTH == False and data_info[0] == "AUTH" and data_info[1] == AUTH_TOKEN:
                    AUTH = True
                    value="****"

                retval = data
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

            source = socket.gethostbyname(socket.gethostname())
            doquery(key, value, source, json.dumps(params))
            connection.sendall(retval)
            logger.debug("Sent data")
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
            doquery(key, value, source, json.dumps(params))
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
