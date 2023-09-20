import RPi.GPIO as GPIO
import smbus2
import time
import math

# Constantes
MT_DEVICE_ADDRESS = 0x06
GPIO_ENA = 11
GPIO_IN1 = 13
GPIO_IN2 = 15
sampleTime = 0.005

# Variables globales
angulo = 0.0
# lastTime = 0.0

# Constantes PID
Kp = 4.249
Kd = 0.14678
Ki = 2.4281e-06

# Variables PID
error = 0.0
error_1 = 0.0
errorI = 0.0
errorD = 0.0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_ENA, GPIO.OUT)
GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)
pwm1 = GPIO.PWM(GPIO_ENA, 1000)
pwm1.start(0)
bus = smbus2.SMBus(1)

def Lectura_MT6701():
    slaveByte1 = bus.read_byte_data(MT_DEVICE_ADDRESS, 0x03)
    slaveByte2 = bus.read_byte_data(MT_DEVICE_ADDRESS, 0x04)
    return (slaveByte1 << 6 or slaveByte2 >> 2) * 360.0 / 16384

def setMotor(valPWM : float, ENA, IN1 : int, IN2 : int):
    dir = True
    if( valPWM < 0 ): dir = False
    valPWM = abs(valPWM)
    if( valPWM > 100 ): valPWM = 100
    #if( valPWM < ZONA_MUERTA ): valPWM = ZONA_MUERTA
    ENA.ChangeDutyCycle(valPWM)
    if( dir ): GPIO.output(IN1, True), GPIO.output(IN2, False)
    else: GPIO.output(IN1, False), GPIO.output(IN2, True)

def calcularPID(setpoint : float, input : float):
    global error, errorI, errorD, error_1
    error = setpoint - input
    errorI += error * sampleTime
    errorD = (error-error_1) / sampleTime
    error_1 = error
    return Kp*error + Ki*errorI + Kd*errorD

while True:
    SP = float(input("set point: "))
    angulo = Lectura_MT6701()
    setMotor( calcularPID(SP, angulo), pwm1, GPIO_IN1, GPIO_IN2 )
    print(angulo)
    time.sleep(0.005)