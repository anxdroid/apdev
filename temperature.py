import datetime
import time
import os
import sqlite3

dbname = '/media/LaCie/Anto/templog.db'

def log_temperature(temp, source):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?), (?))", (temp,source,))

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
	log_temperature(temperature, "28-000003fa0104")
	#temp = str(datetime.datetime.now())+"\t"+str(temperature)+"\n"
	#with open("temp.txt", "a") as myfile:
    	#	myfile.write(temp)

	#print str(datetime.datetime.now())+"\t"+str(temperature)
	#include('testjson.py')
	time.sleep(5)
