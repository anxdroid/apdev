import datetime
import time
import os
import sqlite3
import sys
import Adafruit_DHT

dbname = '/media/LaCie/Anto/templog.db'

def log_reading(value, source, unit):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO sensors (timestamp, value, source, unit) values(datetime('now'), (?), (?), (?))", (value,source,unit,))

    # commit the changes
    conn.commit()

    conn.close()

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

while 1 :
# Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before.
	tfile = open("/sys/bus/w1/devices/28-000003fa0104/w1_slave")
# Read all of the text in the file.
	text = tfile.read()
# Close the file now that the text has been read.
	tfile.close()
# Split the text with new lines (\n) and select the second line.
	secondline = text.split("\n")[1]
# Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
	temperaturedata = secondline.split(" ")[9]
# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
	temperature = float(temperaturedata[2:])
# Put the decimal point in the right place and display it.
	temperature = temperature / 1000
	log_reading(temperature, "TEMP_SALOTTO", "&deg;")

# Humidity

	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
	    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	    if (temperature > 0 and temperature < 50):
	    	log_reading(temperature, "TEMP_DISIMPEGNO", "&deg;")
	    if (humidity > 0 and humidity <= 100):
	    	log_reading(humidity, "UMID_DISIMPEGNO", "%")
	
	time.sleep(30)
