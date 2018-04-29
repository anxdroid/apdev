#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Reconnection script started."
sleep 10

while true
do
	if ! ifconfig | grep --quiet "192.168.1."; then
		echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Not connected..."
		#if iwlist wlan0 scan | grep --quiet "LAN3"; then
		#echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Network is available! Restarting WLAN..."
		ifconfig wlan0 down > /dev/null
		sleep 1
		ifconfig wlan0 up > /dev/null
		sleep 10
		if ifconfig | grep --quiet "192.168.1."; then
			echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Reconnection successful!"
		else
			echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Reconnection failed!"
		fi
	else
		echo `date "+%Y-%m-%d %H:%M:%S" | tr -d '\n'` "Connected... going to sleep for 20s."
		sleep 20
	fi
	sleep 10
done
