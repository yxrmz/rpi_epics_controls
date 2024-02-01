# -*- coding: utf-8 -*-
from softioc import softioc, builder
#import cothread

import RPi.GPIO as GPIO
import time
import numpy as np

currentSteps = 0
stop = False

#GPIO.setmode(GPIO.BOARD)
control_pins = [11, 12, 13, 15]

seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]



def deg_to_steps(deg):
    return int(deg*512/360.)

def steps_to_deg(steps):
    return steps*360/512.

def move_to_position(posDegrees):

    global stop
    global currentSteps
    global pv_fbk
    global status
    global seq
    global control_pins

    if stop:
        stop = False

    posDegrees = float(posDegrees)
    if posDegrees >= 360:
        posDegrees = posDegrees % 360

    posSteps = deg_to_steps(posDegrees)
    print("New position in steps", posSteps)
    deltaSteps = posSteps - currentSteps
    print("Steps to go", deltaSteps)
    rotDir = np.sign(deltaSteps)
    rotVal = np.abs(int(deltaSteps))
    
    GPIO.setmode(GPIO.BOARD)
    for pin in control_pins:
#        print("Setting pin", pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seqOrder = range(8) if rotDir > 0 else range(7, -1, -1)
#    print("Direction seq order", seqOrder)
    status.set(1)
    for i in range(rotVal):
        if stop:
            stop = False
            break
        currentSteps += rotDir
#        print(currentSteps)
        pv_fbk.set(steps_to_deg(currentSteps))
        for halfstep in seqOrder:
            for pin in range(4):
#                print("setting pin", control_pins[pin], "to", seq[halfstep][pin])
                GPIO.output(control_pins[pin], seq[halfstep][pin])
            time.sleep(0.001)
    GPIO.cleanup()
    status.set(0)    

def stop_rotation(val):
    global stop
    if val:
        stop = True

# Set the record prefix
builder.SetDeviceName("LOCAL_SAMPLE_WHEEL")

# Create some records
pv_fbk = builder.aOut('deg:fbk', initial_value=0, always_update=True)
pv_deg = builder.aOut('deg', initial_value=0, always_update=True,
                      on_update=move_to_position)
pv_stp = builder.aOut('stop', initial_value=0, always_update=True,
                      on_update=stop_rotation)
status = builder.mbbIn('status',
                       'MOVE DONE',
                       'MOVING',
                       'ERROR')

# Boilerplate get the IOC started
builder.LoadDatabase()
softioc.iocInit()

# Start processes required to be run after iocInit
#def update():
#    while True:
#        ai.set(ai.get() + 1)
#        cothread.Sleep(1)

#cothread.Spawn(update)

# Finally leave the IOC running with an interactive shell.
softioc.interactive_ioc(globals())
