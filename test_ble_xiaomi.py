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

from lywsd02 import Lywsd02Client

authToken = "0kFamII-GZsJROFdLtSTQsxRUTF9aaQl"
port = 8080
ip = "192.168.1.9"
blynk = blynklib.Blynk(authToken, server=ip, port=port, heartbeat=15)
timer = Timer()

devices = [
    {
        "name" : "camera",
        "mac" : "E7:2E:00:D2:BC:9F",
        "humidity" : 10,
        "temperature" : 11,
        "battery" : 12,
        "type" : "LYWSD02"
    },    
    {
        "name" : "salotto",
        "mac" : "E7:2E:00:B1:C8:80",
        "humidity" : 10,
        "temperature" : 11,
        "battery" : 12,
        "type" : "LYWSD02"
    },
    {
        "name" : "disimpegno",
        "mac" : "58:2D:34:35:2F:02",
        "humidity" : 1,
        "temperature" : 2,
        "battery" : 3,
        "type" : "MJ_HT_V1"
    },
    {
        "name" : "mansarda",
        "mac" : "58:2D:34:35:2E:68",
        "humidity" : 4,
        "temperature" : 5,
        "battery" : 6,
        "type" : "MJ_HT_V1"
    },
    {
        "name" : "terrazzino",
        "mac" : "58:2D:34:36:2F:78",
        "humidity" : 7,
        "temperature" : 8,
        "battery" : 9,
        "type" : "MJ_HT_V1"
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

@timer.register(interval=5)
def readVal():
    #print("Polling...")
    for device in devices :
        try:
            print("Polling from "+device["mac"]+" of type "+device["type"])
            """Poll data from the sensor."""
            if (device["type"] == "MJ_HT_V1") :
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
            if (device["type"] == "LYWSD02") :
                client = Lywsd02Client(device["mac"])
                print("Battery: {}".format(client.battery))
                temperature = float(client.temperature)
                print("Temperature: "+str(temperature))
                blynk.virtual_write(device["temperature"], temperature)
                humidity = float(client.humidity)
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
