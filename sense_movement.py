#!/usr/bin/env/python

import RPi.GPIO as GPIO
import blink
import time, os, random
from sys import exit

LEFT_LED = 24
RIGHT_LED = 23
PIR_POWER = 17
PIR_OUT = 4  

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR_OUT, GPIO.IN)
GPIO.setup(PIR_POWER, GPIO.OUT)
GPIO.setup(LEFT_LED, GPIO.OUT)
GPIO.setup(RIGHT_LED, GPIO.OUT)

GPIO.output(PIR_POWER, GPIO.HIGH)

sounds = os.listdir(os.path.join(os.getcwd(), 'sounds'))

def play_sound():
    num = random.randint(0, len(sounds) - 1)
    fname = os.path.join('sounds', sounds[num])
    cmd = 'mpg321 -g 500 %s &' % fname
    os.system(cmd)

def main():
    time.sleep(10)

    while 1:
        movement = GPIO.input(4)
        try:
            if movement == True:
                print "I sense movement!!!"
                play_sound()
                #blink.multi_blinks(blink.pattern02)
                blink.dual_blink(RIGHT_LED, LEFT_LED, blink.VERY_FAST,
                                 repeat=100)
                time.sleep(10)
            else:
                print "."
                time.sleep(5)

        except KeyboardInterrupt:
            break

    GPIO.cleanup()
    exit()

if __name__ == '__main__':
    main()
