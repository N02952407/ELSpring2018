# CPS342 Embedded Linux Project: Camera Boom

For this project we developed a design where we used a Raspberry Pi 3 and a Pi camera to take still pictures through a web interface. Our goal was to use two servo motors to create a platform that had the camera attached to it and using the web interface, we controlled the servo motors to rotate the camera, take still pictures, and display them to the web interface.

The hardware part of the project was getting the two continuous rotation servo motors (FeeTech FS5103R) to work with Pi using Adafruit 16-Channel 12-bit PWM/Servo Driver (PCA9685). The servo driver had to be soldered and then connect to the Pi using female to female jumper cables. Using this type of cable made it possible for us to eliminate the breadboard. The connections between the Pi and the driver were the VCC to 3.3V power supply on the pi, GND to one of the GND connections, SCL to SCL1 pin and SDA to SDA1 pin on the Pi. After this One of the servo motors was connected to Channel 0 and the other one was connected to Channel 1 on the servo driver. 

Once both the hardware and software was ready, we managed to successfully implement the project. The two servos were attached to each other using Velcro and a small 3D printed boom hinge was attached to the top servo to make it easier to attach the camera. The web interface has sliders that controls the servo motors. The top motor was set to a virtual limit of approximately 90 degrees while the other was set to a virtual limit of  180 degrees. In addition to sliders, there are also reset buttons to reset the servo motors back to their starting point. Lastly, the “Take a Picture” button allows the user to take a picture at any point and gives a link to the picture with time & date stamp in addition to the servo’s location in degrees when the camera was taken. 

The final step was the overall cleanliness of the executed design. We troubleshooted the range of motion for the two servos by making sure the tension on the wires was neither too taught nor too loose. Additionally, we ensured that there were no obstacles in the way of the actual path of each servos. The html script limited our range of motion to be practical with our setup, so it is already worked into the system that our servos won’t push anything out of their comfortable range of motion. 

For final bugs, there was a slight inconsistency for both servos when we inputted the minimum rotational command for the counter clockwise direction. Instead of moving slightly counter clockwise when inputting a small degree movement under 7 degrees, our servos would simply move 7 degrees or more clockwise. So in order to calibrate this, we used an ad hoc method of simply ensuring the counter clockwise command sent a minimum pwm signal of .02 or greater, i.e. implementing an additional if else statement for adding .02 to the pwm of any counterclockwise input. This took care of the problem 100% of the time, but you can still notice the servos having the slightest minimal clockwise rotation executed before every command which we could not prevent. A step motor would definitely help with this problem in the future.


## Installation

First, install the Adafruit PCA9685 PWM servo/LED controller by running the following command:

sudo pip install adafruit-pca9685

Next, install Flask and camera dependencies using:

	sudo apt-get install python3-flask python3-picamera

After, edit line 27 of FinalServos.py and set BASE_DIR to the directory where you would like your images to be saved. Then, edit line 134 to your Pi's IP address and execute FinalServos with:

	sudo python FinalServos.py


## Work Division

Cory Boris: 33.3 %

Cansu Çabuk: 33.3 %

Emil Padikkala: 33.3 %
