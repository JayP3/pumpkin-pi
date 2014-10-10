import RPi.GPIO as GPIO
import time


def simple_blink(pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)

def complex_blink(pin, on_time, off_time):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(on_time)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(off_time)

def repeated_blink(pin, duration, repeat=1):
    i = 0
    while i < repeat:
        simple_blink(pin, duration)
        simple_blink(pin, duration)
        complex_blink(pin, duration * 4, duration)
        i += 1

def dual_blink(pin1, pin2, duration, repeat=1):
    for i in range(0, repeat):
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        time.sleep(duration)   

def multi_blink(((pins), duration, rest)):
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
    if rest:
        time.sleep(rest)

def multi_blinks(pattern, repeat=1):
    """
    pattern is a list or tuple, where each element is ((pins), duration, rest)
    """
    for r in range(0, repeat):
        for i in pattern:
            multi_blink(i)

# Blink Speeds
VERY_FAST = 0.125
FAST = 0.25
MEDIUM = 0.5
SLOW = 1
VERY_SLOW = 2
# Pin Numbers
RIGHT_LED = 25
LEFT_LED = 18

rightblnk_M = ((RIGHT_LED,), MEDIUM, 0)
left_blnk_M =   ([LEFT_LED], MEDIUM, 0)
rightblnk_F = ((RIGHT_LED,), FAST, 0)
left_blnk_F =   ([LEFT_LED], FAST, 0)
dl_blnk_F = ((LEFT_LED, RIGHT_LED), FAST, FAST)
dl_blnk_S = ((LEFT_LED, RIGHT_LED), SLOW, SLOW)

pattern01 = (
             rightblnk_M, left_blnk_M, rightblnk_M,
             left_blnk_M, dl_blnk_F, dl_blnk_F, 
             dl_blnk_F, dl_blnk_F
             )


pattern02 = (
            dl_blnk_F, rightblnk_F, left_blnk_F, dl_blnk_F
            )
            
pattern02 = (
            dl_blnk_F, 
            )