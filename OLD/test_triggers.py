import multiprocessing
import sqlite3
import time
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
    logger = logging.getLogger("process-triggers")
    logger.debug("Starting thresholds process")
    conn=sqlite3.connect(dbname)
    try:   
        curs=conn.cursor()
        logging.info("Querying...")
        for row in curs.execute("SELECT * FROM thresholds WHERE active = 1 AND id = ?", (id, )):
            print row
            if str(row[1]) in values:
                print row[1]+" "+str(row[2])+" "+str(row[3])+" "+str(values[str(row[1])])
                if (values[str(row[1])] >= row[2] and values[str(row[1])] <= row[3]):
                    return True
            return False
            logger.debug("Done threshold id %d", row[0])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing thresholds process")
        conn.close()    

def triggers():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-triggers")
    logger.debug("Starting triggers process")
    conn=sqlite3.connect(dbname)
    try:   
        curs=conn.cursor()
        logging.info("Querying...")
        for row in curs.execute("SELECT * FROM triggers WHERE active = 1"):
            #print row
            trigger = str(row[1])
            p = re.compile('\d+')
            ids = p.findall(trigger)
            print ids
            for id in ids:
                check = check_threshold(id)
                trigger = trigger.replace(str(id), str(check))
                #print check
            print trigger
            check = eval(trigger)
            print(check)
            logger.debug("Done trigger id %d", row[0])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing triggers process")
        conn.close()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting...")

    values['TEMP_SALOTTO'] = 16.5
    values['TEMP_ESTERNA'] = 5
	values['HOURS'] = 18
    process_triggers = multiprocessing.Process(target=triggers, args=())
    process_triggers.start()
    logging.info("...done !")
    logging.info("All done")
