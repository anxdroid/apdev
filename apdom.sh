#!/bin/bash
python /home/osmc/test_sensors.py & &> sensors.log
python /home/osmc/test_server.py & &> server.log

