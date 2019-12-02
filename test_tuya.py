import blynklib
from blynktimer import Timer
import argparse
import re
import time
import logging
import sys
import httplib2
import hashlib
import json
import pytuya

current_milli_time = lambda: int(round(time.time() * 1000))

authToken = "0fce7beae9ac41108abc385687adb76f"
port = 8080
ip = "192.168.1.9"
blynk = blynklib.Blynk(authToken, server=ip, port=port, heartbeat=30)
timer = Timer()

devices = [
    {
        "name" : "Condizionatore Mansarda",
        "ip" : '192.168.1.11',
        "id" : "04564850840d8e9bb04b",
        "key" : "68a760c04fd5ce1f",
        "vpin" : 1
    },
    {
        "name" : "Termodinamico",
        "ip" : '192.168.1.8',
        "id" : "20856001cc50e3d2a7d9",
        "key" : "60ef17b549d76787",
        "vpin" : 2
    },
]

CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'

@blynk.handle_event("connect")
def connect_handler():
    print(CONNECT_PRINT_MSG)

@blynk.handle_event("disconnect")
def disconnect_handler():
    print(DISCONNECT_PRINT_MSG)
    blynk.connect()

@timer.register(interval=10)
def readVal():
    for device in devices :
        try:
            print("Polling from "+device["name"]+" on vpin "+str(device["vpin"]))
            d = pytuya.OutletDevice(device["id"], device["ip"], device["key"])
            data = d.status()  # NOTE this does NOT require a valid key
            print('Dictionary %r' % data)
            print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device
            output = str(data['dps']['5'])
            print(output)
            if (output is not None and output.isnumeric()) :
                print('Output: ', output)
                val = float(output)
                val /= 1000
                print('Sending: ', val)
                blynk.virtual_write(device["vpin"], str(val))
            
        except Exception as e:
            print (e)

def main():
    #sys.stdout = open("/var/log/domotic.log", "w", buffering=2)
    #readVal()
    while True:
        blynk.run()
        timer.run()

if __name__ == "__main__":
		main()
