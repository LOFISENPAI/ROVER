#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from appCam import VideoCamera
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import time
import threading
import os
import curses

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

#Define Motor Driver GPIO pins
# Motor A, LEFT
PWM_DRIVE_LEFT = 21     # PWMA - H-Bridge enable pin
FORWARD_LEFT_PIN = 16   # AI1 - Forward Drive
REVERSE_LEFT_PIN = 20   # AI2 - Reverse Drive
# Motor B, RIGHT
PWM_DRIVE_RIGHT = 5     # PWMB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 19  # BI1 - Forward Drive
REVERSE_RIGHT_PIN = 13  # BI2 - Reverse Drive

# Initialise objects for H-Bridge GPIO PWM pins
# Use defaults for initial duty cycle - 0 and frequency=100Hz
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT)

# Initialise objects for H-Bridge digital GPIO pins
forwardLeft = DigitalOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = DigitalOutputDevice(REVERSE_LEFT_PIN)
forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/allStop')
def allStop():
    forwardLeft.off()
    reverseLeft.off()
    forwardRight.off()
    reverseRight.off()
    driveLeft.value = 0
    driveRight.value = 0
    return render_template('index.html')

@app.route('/forwardDrive')
def forwardDrive():
    forwardLeft.on()
    reverseLeft.off()
    forwardRight.on()
    reverseRight.off()
    driveLeft.value = 0.5
    driveRight.value = 0.5
    return render_template('index.html')

@app.route('/reverseDrive')
def reverseDrive():
    forwardLeft.off()
    reverseLeft.on()
    forwardRight.off()
    reverseRight.on()
    driveLeft.value = 0.6
    driveRight.value = 0.6
    return render_template('index.html')

@app.route('/spinLeft')
def spinLeft():
    forwardLeft.off()
    reverseLeft.on()
    forwardRight.on()
    reverseRight.off()
    driveLeft.value = 0.2
    driveRight.value = 0.7
    return render_template('index.html')

@app.route('/spinRight')
def spinRight():
    forwardLeft.on()
    reverseLeft.off()
    forwardRight.off()
    reverseRight.on()
    driveLeft.value = 0.7
    driveRight.value = 0.2
    return render_template('index.html')

@app.route('/backLeft')
def backLeft():
    forwardLeft.off()
    reverseLeft.on()
    forwardRight.off()
    reverseRight.on()
    driveLeft.value = 0.2
    driveRight.value = 0.6
    return render_template('index.html')

@app.route('/backRight')
def backRight():
    forwardLeft.off()
    reverseLeft.on()
    forwardRight.off()
    reverseRight.on()
    driveLeft.value = 0.6
    driveRight.value = 0.2
    return render_template('index.html')

@app.route("/<action>")
def action(action):
    if action == "forwardDrive":
        forwardDrive()
        allStop()
    if action == "reverseDrive":
        reverseDrive()
        allStop()
    if action == "spinLeft":
        spinLeft()
        allStop()
    if action == "spinRight":
        spinRight()
        allStop()
    if action == "backLeft":
        backLeft()
        allStop()
    if action == "backRight":
        backRight()
        allStop() 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)