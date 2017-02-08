from picamera import PiCamera
from os import system
from time import sleep

camera = PiCamera()
camera.resolution = (1024, 768)

for i in range(80):
	print("Taking photo")
	camera.capture('/home/pi/timelapse/image{0:04d}.jpg'.format(i))
	sleep(60*15)
#print("Making gif...")
#system('convert -delay 10 -loop 0 /home/pi/timelapse/image*.jpg /home/pi/timelapse/animation.gif')
print("done !")
