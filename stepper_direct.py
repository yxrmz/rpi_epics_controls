import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
control_pins = [11,12,13,15]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]
for i in range(512):
  for halfstep in range(8): #(7, -1, -1):
    for pin in range(3, -1, -1):
      GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    time.sleep(0.001)
GPIO.cleanup()
