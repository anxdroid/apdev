import multiprocessing
import sqlite3
import time
import re
import crypt
import random
import hashlib
from passlib.apache import HtpasswdFile
from passlib.hash import apr_md5_crypt

dbname = '/media/LaCie/Anto/templog.db'

def salt():
    """Returns a string of 2 randome letters"""
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789/.'
    return random.choice(letters) + random.choice(letters)

def auth(username, password):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-auth")
    logger.debug("Starting auth process")
    conn=sqlite3.connect(dbname)
    try:   
        curs=conn.cursor()
        logging.info("Querying...")
	#print crypt.crypt(password, salt())
        #print hashlib.md5(password).hexdigest()
	#ht = HtpasswdFile()
	#ht.set_password(username, password)
	#print ht.to_string()
	#h = md5_crypt.hash(password)
	#print h
	print apr_md5_crypt.hash(password)
	for row in curs.execute("SELECT password FROM users WHERE username = ?", (username, )):
        	print row[0].replace('$apr1$', '$1$')
		print apr_md5_crypt.verify(password, row[0])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing triggers process")
        conn.close()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    auth('anto', 'resistores')
    logging.info("All done")
