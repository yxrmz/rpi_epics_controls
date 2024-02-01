import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
control_pins = [16, 18, 22]

pwm_time = 0.001

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
GPIO.output(control_pins[2], 1)

#halfstep_seq = [
#  [1,0,0,0],
#  [1,1,0,0],
#  [0,1,0,0],
#  [0,1,1,0],
#  [0,0,1,0],
#  [0,0,1,1],
#  [0,0,0,1],
#  [1,0,0,1]
#]
for i in range(2048*4):
    GPIO.output(control_pins[0], 1)
#  for halfstep in range(8): #(7, -1, -1):
#    for pin in range(3, -1, -1):
#      GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    time.sleep(pwm_time)
    GPIO.output(control_pins[0], 0)
    time.sleep(pwm_time)
GPIO.output(control_pins[2], 0)
#
