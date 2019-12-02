import blynklib
from blynktimer import Timer
import argparse
import re
import time
import logging
import sys

from btlewrap import available_backends, BluepyBackend, GatttoolBackend, PygattBackend
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, \
    MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY

authToken = "08dbf62f92b64b34ae4b33ae69d2d530"
port = 8080
ip = "192.168.1.9"
blynk = blynklib.Blynk(authToken, server=ip, port=port, heartbeat=15)
timer = Timer()

"""
    {
        "name" : "terrazzino",
        "mac" : "",
        "humidity" : 7,
        "temperature" : 8,
        "battery" : 9
    },
"""

devices = [
    {
        "name" : "salotto",
        "mac" : "58:2D:34:35:2F:02",
        "humidity" : 1,
        "temperature" : 2,
        "battery" : 3
    },
    {
        "name" : "mansarda",
        "mac" : "58:2D:34:35:2E:68",
        "humidity" : 4,
        "temperature" : 5,
        "battery" : 6
    }
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

@timer.register(interval=5)
def readVal():
    #print("Polling...")
    for device in devices :
        try:
            print("Polling from "+device["mac"])
            """Poll data from the sensor."""
            poller = MiTempBtPoller(device["mac"], GatttoolBackend, retries=1)
            #print("Getting data from Mi Temperature and Humidity Sensor")
            #print("FW: {}".format(poller.firmware_version()))
            #print("Name: {}".format(poller.name()))
            print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))
            temperature = float(poller.parameter_value(MI_TEMPERATURE))
            print("Temperature: "+str(temperature))
            blynk.virtual_write(device["temperature"], temperature)
            humidity = float(poller.parameter_value(MI_HUMIDITY))
            print("Humidity: "+str(humidity))
            blynk.virtual_write(device["humidity"], humidity)
        except Exception as e:
            print (e)

def main():
    #sys.stdout = open("/var/log/domotic.log", "w", buffering=2)
    while True:
        blynk.run()
        timer.run()

if __name__ == "__main__":
		main()
