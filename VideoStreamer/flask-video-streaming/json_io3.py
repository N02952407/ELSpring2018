#!flask/bin/python

import sys, re, json, picamera
import flask
from flask import Flask, render_template, request, redirect, Response
from camera_pi import Camera
import servo

resultY = "45"
resultX = "90"
app = Flask(__name__)

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
    receieve_inputX(degrees2, resultX)
    resultX = request.form['data']
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



if __name__ == '__main__':
	# run!
	app.run(host = '137.140.182.34', threaded='true', debug = 'true')
