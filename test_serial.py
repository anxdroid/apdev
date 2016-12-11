import serial
import MySQLdb
import time
import re
import datetime

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

def main ():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    while True:
        p = re.compile('\d+')
        vals = p.findall(ser.readline())
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        for val in vals:
            print st+" "+str(val)
            #print ser.readline()
        time.sleep(1)

if __name__ == "__main__":
        main()
