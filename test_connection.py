from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gas_leakage = 27
intruder = 22

GPIO.setup(gas_leakage, GPIO.IN)
GPIO.setup(intruder, GPIO.IN)


def convert(x):
    """converts 0 to 1 and 1 to 0"""
    if x == 0:
        return 1
    if x == 1:
        return 0


while True:
    try:
        if  convert(GPIO.input(gas_leakage)):
            print('There is fire')
            sleep(1)
        if convert(GPIO.input(intruder)):
            print('Intruder Alert')
            sleep(1)
    except Exception as e:
        print(str(e))
        GPIO.cleanup()
