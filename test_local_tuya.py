
import argparse
import re
import time
import logging
import sys

import hashlib
import json
import pytuya

current_milli_time = lambda: int(round(time.time() * 1000))

devices = [
    {
        "name" : "Condizionatore Mansarda",
        "ip" : '192.168.1.81',
        "id" : "04564850840d8e9bb04b",
        "key" : "68a760c04fd5ce1f",
        "vpin" : 1
    },
    {
        "name" : "Termodinamico",
        "ip" : '192.168.1.82',
        "id" : "20856001cc50e3d2a7d9",
        "key" : "60ef17b549d76787",
        "vpin" : 2
    },
]

def readVal():
    for device in devices :
        try:
            print("Polling from "+device["name"]+" on vpin "+str(device["vpin"]))
            d = pytuya.OutletDevice(device["id"], device["ip"], device["key"])
            data = d.status()  # NOTE this does NOT require a valid key
            print('Dictionary %r' % data)
            print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device
            output = str(data['dps']['4'])
            print(output)
            if (output is not None and output.isnumeric()) :
                print('Output: ', output)
                val = float(output)
                val /= 1000
                print('Sending: ', val)

        except Exception as e:
            print (e)

def main():
    readVal()

if __name__ == "__main__":
		main()
