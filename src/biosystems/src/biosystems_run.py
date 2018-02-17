#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64MultiArray,Float32MultiArray,String
import numpy as np
import signal
import sys
import time
import RPi.GPIO as GPIO
#-----------------------------------------------------------------
#SIGINT handler

def sigint_handler(signal, frame):
	sys.exit(0)

def update():
	global drill , height
	if(drill==1):
		GPIO.output(12, GPIO.HIGH) # Set AIN1
		GPIO.output(11, GPIO.LOW) # Set AIN2
		drill1.ChangeDutyCycle(0.7*255)
	elif(drill==-1):
		GPIO.output(11, GPIO.HIGH) # Set AIN1
		GPIO.output(12, GPIO.LOW) # Set AIN2
		drill1.ChangeDutyCycle(0.7*255)
	else:
		GPIO.output(12, GPIO.LOW) # Set AIN1
		GPIO.output(11, GPIO.LOW) # Set AIN2
		drill1.ChangeDutyCycle(0)	
	if(height==1):
		GPIO.output(15, GPIO.HIGH) # Set AIN1
		GPIO.output(16, GPIO.LOW) # Set AIN2
		height1.ChangeDutyCycle(0.7*255)
	elif(height==-1):
		GPIO.output(16, GPIO.HIGH) # Set AIN1
		GPIO.output(15, GPIO.LOW) # Set AIN2
		height1.ChangeDutyCycle(0.7*255)
	else:
		GPIO.output(15, GPIO.LOW) # Set AIN1
		GPIO.output(16, GPIO.LOW) # Set AIN2	
		height1.ChangeDutyCycle(0)



def bio_callback(inp):
	global drill , height
	#print("callback\n")
	#print(inp)
	#print(inp.data)
	drill = inp.data[6]
	height = inp.data[3]
	#print(inp.data[6])
	#print(inp.data[3])


if __name__ == '__main__':

	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(12, GPIO.OUT) # Connected to drillIN1
	GPIO.setup(11, GPIO.OUT) # Connected to drillIN2
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT) # Connected to heightIN1
	GPIO.setup(16, GPIO.OUT) # Connected to heightIN2
	GPIO.setup(13, GPIO.OUT)
	
	drill1=GPIO.PWM(18,255)
	height1=GPIO.PWM(13,255)

	drill=0
	height=0
	
	rospy.init_node('bio', anonymous=True)
	rospy.Subscriber("/rover/control_directives", Float64MultiArray, bio_callback)
	
	signal.signal(signal.SIGINT, sigint_handler)
	while(True):
		update()	