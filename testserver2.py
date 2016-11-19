import multiprocessing
import socket
import RPi.GPIO as GPIO

AUTH_TOKEN = "f_Yhkoljlj43_."

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
            if AUTH == False and data_info[0] == "AUTH" and data_info[1] == AUTH_TOKEN:
                AUTH = True
            
            if AUTH == False:
                logger.debug("Failed auth !")
                data = "Get out !"
            elif data_info[0] != "AUTH" :
                if (data_info[0] == "RELAY"):
                    data = RELAY(data_info[1], logger)
                else :
                    logger.debug("Unknown command !")
                    data = "Unknown command !"
            else:
                logger.debug("Authenticated !")
                data = "Welcome !"

            connection.sendall(data)
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
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == "__main__":
    import logging
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 82)
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
        GPIO.cleanup()
    logging.info("All done")