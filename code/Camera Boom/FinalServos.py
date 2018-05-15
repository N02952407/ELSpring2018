#!flask/bin/python
import sys, re, json, picamera, datetime, time, os, flask, servos_commands
from flask import Flask, render_template, request, redirect, Response, send_file, abort

import Adafruit_PCA9685
from Adafruit_GPIO.GPIO import*

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(0X40)
pwm.set_pwm_freq(50)

resultY = "45" #initialize global variable for y-axis resting position
resultX = "90" #" " x-axis " "
app = Flask(__name__)

@app.route('/', defaults={'req_path': ''}, methods =['GET'])
@app.route('/<path:req_path>') # set path
def output(req_path):
	# serve index template
	global resultY
	global resultX
	# declare directory for images
	BASE_DIR = '/home/CoryBoris/Adafruit_Python_PCA9685/images'
	abs_path = os.path.join(BASE_DIR, req_path)
	# case if path does not exist
	if not os.path.exists(abs_path):
		return abort(404)
	# case to send files in directory to page
	if os.path.isfile(abs_path):
		return send_file(abs_path)
	# variables for HTML
	files = os.listdir(abs_path)
	return render_template('index.html', files=files, keyY = "The Y-Axis Servos is at: " + resultY + " degrees", keyX = "The X-Axis Servos is at: " + resultX + " degrees", testY = resultY, testX = resultX)

@app.route('/receiverY', methods =['POST'])
def receiverY():
	# read json + reply
    print(request.form['data']+ " Degrees at Y-Axis ") #this is a test case to the terminal console
    global resultY
    degrees_2Y = request.form['data']
    
    def receive_inputY(degrees_2Y, resultY):
            flag = 0
            R = float(degrees_2Y) - float(resultY)
            print(str(R)+" this is an indicator")
            output = R/900
            if(R > 0):
                flag = 12 #clockwise
            else:
                flag = 475 #counterclockwise
                print(output)
                output = -output + 0.025
            print("Y pwm = " + str(output))
            pwm.set_pwm(1, 0, flag)
            time.sleep(output)
            pwm.set_pwm(1, 0, 0)
            print("servos moved to: " + degrees_2Y)
            return "true"
    receive_inputY(degrees_2Y, resultY)
    
    resultY = request.form['data'] # this ensures result points to the form data of the slider
    
    if resultY == "1":
        return "The Y-Axis Servos is at: " + resultY + " degree"
    else:
        return "The Y-Axis Servos is at: " + resultY + " degrees"
		
@app.route('/receiverX', methods =['POST'])
def receiverX():
	# read json + reply
    print(request.form['data'] + " Degrees at X-Axis ") #this is a test case to the terminal console
    global resultX
    degrees_2X = request.form['data']
    
    def receive_inputX(degrees_2X, resultX):
        flag = 0
        R = float(degrees_2X) - float(resultX)
        output = R/720
        print(str(R)+" this is an indicator")
        if(R > 0.0):
            print("This is the if, it should be clockwise")
            flag = 12 #clockwise
        else:
            print("This is the else, it should be counterclockwise")
            flag = 475 #counterclockwise
            output = -output + 0.025
        
        print("X pwm = " + str(output))
        print(flag)
        pwm.set_pwm(0, 0, flag)
        time.sleep(output)
        pwm.set_pwm(0, 0, 0)
        print("servos moved to: " + degrees_2X)
        return "true"
    
    receive_inputX(degrees_2X, resultX)
    resultX = request.form['data'] #update global resultX for template
    if resultX == "1":
        return "The X-Axis Servos is at: " + resultX + " degree"
    else:
        return "The X-Axis Servos is at: " + resultX + " degrees"

# Picture taking function
@app.route('/takePic', methods =['POST'])
def takePic():
		# variables to save boom position
        global resultY
        global resultX
		# creates string for time stamp of picture
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
		# open camera instance and save photo with time stamp and coordinates
        with picamera.PiCamera() as camera:
            camera.resolution = (640,480)
            camera.capture("/home/CoryBoris/Adafruit_Python_PCA9685/images/"+date+"_Y-axis: " + resultY + "_X-axis: " + resultX +".jpg")
        TPmessage = "Picture Taken"
        print("OK")
        return 'OK'

if __name__ == '__main__':
	# Replace the host IP with your own
	app.run(host = '137.140.182.58', threaded='true')