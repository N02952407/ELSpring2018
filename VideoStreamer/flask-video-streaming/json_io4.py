#!flask/bin/python
from __future__ import division
import sys, re, json, picamera
import flask
from flask import Flask, render_template, request, redirect, Response
from camera_pi import Camera

import Adafruit_PCA9685
from Adafruit_GPIO.GPIO import *





import time





# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(0X40)

resultY = "45"
resultX = "90"
app = Flask(__name__)
pwm.set_pwm_freq(60)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods =['GET'])
def output():
	# serve index template
    global resultY
    global resultX
    return render_template('index_test.html', keyY = "The Y-Axis Servos is at: " + resultY + " degrees", keyX = "The X-Axis Servos is at: " + resultX + " degrees", testY = resultY, testX = resultX)

@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/receiverY', methods =['POST'])
def receiverY():
	# read json + reply
    print(request.form['data']+ " Degrees at Y-Axis ") #this is a test case to the terminal console
    global resultY
    resultY = request.form['data'] # this ensures result points to the form data of the slider
    #do something here with the data, aka, send the degrees as parameters to a function which converts
    #the degres to pwm and back to degrees
    #return result
    
    if resultY == "1":
        
        return "The Y-Axis Servos is at: " + resultY + " degree"
    else:
        return "The Y-Axis Servos is at: " + resultY + " degrees"

@app.route('/receiverX', methods =['POST'])
def receiverX():
	# read json + reply
    print(request.form['data'] + " Degrees at X-Axis ") #this is a test case to the terminal console
    global resultX
    degrees2 = request.form['data']
    #receieve_inputX(degrees2, resultX) #send degrees and make servos move
    resultX = request.form['data'] #update global resultX for template
    if resultX == "1":
        return "The X-Axis Servos is at: " + resultX + " degree"
    else:
        return "The X-Axis Servos is at: " + resultX + " degrees"

@app.route('/takePic', methods =['POST'])
def takePic():
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.capture("/home/pi/ClassCode/final/flask-video-streaming/image.jpg")
	TPmessage = "Picture Taken"
	print("OK")
	return 'OK'

def receive_inputX(degrees_2, resultX) :
    flag = 0
    R = degrees_2 - resultX
    output = 0.24 * R
    if(R > 0):
	    flag = 12 #clockwise
    else:
	    flag = 475 #counterclockwise

    pwm.set_pwm(0, 0, flag)
    time.sleep(output)
    pwm.set_pwm(0, 0, 0)
    print("servos moved to: " + degrees_2)
    return "true"


if __name__ == '__main__':
	# run!
	app.run(host = '192.168.0.16', threaded='true', debug = 'true')
