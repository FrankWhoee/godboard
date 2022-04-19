import time
import RPi.GPIO as GPIO
from ADCDevice import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

adc = ADCDevice()  # Define an ADCDevice class object


def setup():
    global adc
    if (adc.detectI2C(0x48)):  # Detect the pcf8591.
        adc = PCF8591()
    elif (adc.detectI2C(0x4b)):  # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
              "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
              "Program Exit. \n")
        exit(-1)


def loop():
    pressed = False
    while True:
        if not pressed and not GPIO.input(25):
            pressed = True
            value = adc.analogRead(0)  # read the ADC value of channel 0
            parseToChar(value, delete=True)
        else:
            pressed = False
        value = adc.analogRead(0)
        parseToChar(value)
        time.sleep(0.1)
        print("\b", end="")

def parseToChar(value, delete=False):
    if value == 0:
        print(" ", end="")
    elif value == 255 and delete:
        print("\b", end="")
    else :
        print(chr(int(value * 25 / 255) + 0x41), end="")

def destroy():
    adc.close()


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()