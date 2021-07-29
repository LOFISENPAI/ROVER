#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from appCam_edit import Camera
from gpiozero import Servo, Robot
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep
import time
import threading
import os
import curses

pi_camera = Camera(flip=False) # flip pi camera if upside down.

# MOTOR A - LEFT SIDE GPIO CONSTANTS
PWML = 21           # PWMA - H-bridge enable pin
FL = 16             # AI1 - forward drive
RL = 20             # AI2 - reverse drive
# MOTOR B - RIGHT SIDE GPIO CONSTANTS
PWMR = 5            # PWMB - H-bridge enable pin
FR = 19             # BI1 - forward drive
RR = 13             # BI2 - reverse drive
# OTHER SENSORS
#ECHO = 23           # echo pin on distance sensor
#TRIG = 24           # trigger pin on distance sensor
#RDISK = 17          # encoder disk on the right rear wheel
PANPIN = 25         # pan servo
TILTPIN = 27        # tilt servo

#set pin factory for servos and create objects of the Servo class
ping_fac = PiGPIOFactory()
pan = Servo(PANPIN, pin_factory = ping_fac)
tilt = Servo(TILTPIN,pin_factory = ping_fac)

# rover controls
rover = Robot((FL,RL,PWML), (FR,RR,PWMR))

# FWD/BACK SPEED, TURN SPEED, CURVE SPEED
FSPD = 0.5
BSPD = 0.6
TSPD = 0.7
CSPD = 1.0

# APP GLOBALS (DO NOT EDIT)
app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')
    
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    # DEVICES
    if deviceName == 'pan':
        actuator = pan
    if deviceName == 'tilt':
        actuator = tilt
    if deviceName == 'rover':
        actuator = rover
    # ACTIONS
    if action == "max":
        if actuator.value < 1:
            actuator.value += 0.2
    if action == "min":
        if actuator.value > -1:
            actuator.value -= 0.2
    if action == "mid":
        actuator.mid()
    if action == "forward":
        actuator.forward(FSPD)
    if action == "backward":
        actuator.backward(BSPD)
    if action == "stop":
        actuator.stop()
    if action == "left":
        actuator.left(TSPD)
    if action == "right":
        actuator.right(TSPD)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)