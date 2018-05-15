# Remote Controlled Pi Camera
A python application to remotely control a Raspberry Pi Camera attached to servos. Images are contained in /docs folder.

## Installation

First, install the Adafruit PCA9685 PWM servo/LED controller by running the following commands:

    sudo pip install adafruit-pca9685
	
Next, install Flask and camera dependencies using:

	sudo apt-get install python3-flask python3-picamera

After, edit line 27 of FinalServos.py and set BASE_DIR to the directory where you would like your images to be saved. Then, edit line 134 to your Pi's IP address and execute FinalServos with:

	sudo python FinalServos.py
