#!/bin/bash
while true
	do
		echo "Start..."
		python3 /home/pi/apdev/test_abb2.py
		echo "End..."
		rm -rf /home/pi/apdev/.cache/
	done
