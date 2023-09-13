import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(37, gpio.OUT)
gpio.setup(36, gpio.OUT)
gpio.setup(35, gpio.OUT)

pin1 = gpio.PWM(37, 1000)
pin1.start(0)
pin2 = gpio.PWM(36, 1000)
pin2.start(0)
pin3 = gpio.PWM(35, 1000)
pin3.start(0)

while True:
    for i in range(100, -1, -1):
        pin1.ChangeDutyCycle(i)
        pin2.ChangeDutyCycle(100 - i)
        pin3.ChangeDutyCycle(i)

        time.sleep(0.02)
    for i in range(1, 101, 1):
        pin1.ChangeDutyCycle(i)
        pin2.ChangeDutyCycle(100 - i)
        pin3.ChangeDutyCycle(i)
        time.sleep(0.02)
    print("Ciclo completo")