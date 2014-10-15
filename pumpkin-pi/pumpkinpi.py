import time
import random
import os
import threading
import RPi.GPIO as GPIO

LEFT_LED = 24
RIGHT_LED = 23
PIR_POWER = 17
PIR_SENSE = 4

# Blink Speeds
VERY_FAST = 0.125
FAST = 0.25
MEDIUM = 0.5
SLOW = 1
VERY_SLOW = 2

pins = {LEFT_LED:  (GPIO.OUT, 'LED'),
        RIGHT_LED: (GPIO.OUT, 'LED'),
        PIR_POWER: (GPIO.OUT, 'SENSOR_POWER'),
        PIR_SENSE: (GPIO.IN,  'SENSOR')
        }


class PumpkinPi(object):
    """Controls the blinking lights, PIR motion sensor, and sounds.
    """
    def __init__(self, mode, pins):
        """Initialize a PumpkinGPIO object"""
        self.kill_thread = threading.Event()
#        self.gpio = PumpkinGPIO(mode, pins)
        self.mode = mode
        self.pins = pins
        self.setup_pins(mode, pins)

    def run(self):
        self.kill_thread.clear()
        t = Watcher(self, self.kill_thread)
        t.start()
        self.loop_thread = t

    def stop(self):
        print "Killing the Watcher thread"
        self.kill_thread.set()

    def blink_lights(self):
        pass

    def multi_blink(self, pins, duration, repeat=1):
        for i in range(0, repeat):
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)
            time.sleep(duration)

    def play_sound(self):
        sounds = os.listdir(os.path.join(os.getcwd(), 'sounds'))
        num = random.randint(0, len(sounds) - 1)
        fname = os.path.join('sounds', sounds[num])
        cmd = 'mpg321 -g 500 %s &' % fname
        os.system(cmd)

    def setup_pins(self, mode, pins):
        """Set up pins for input or output.
        Arguments:
          mode       : Either GPIO.BCM or GPIO.BOARD
          pins (dict): A dictionary of pin numbers and pin setup,
                      (GPIO.IN or GPIO.OUT.
        """
        GPIO.setmode(mode)
        for pin in pins.keys():
            GPIO.setup(pin, pins[pin][0])

    def cleanup_gpio():
        GPIO.cleanup()


class PumpkinGPIO(object):
    """This is where all the info regarding what is connected
    to the GPIO pins on the Raspberry Pi.
    Valid GPIO pins are:
        *****Raspberry Pi Model B (4, 17, 18, 21, 22, 23, 24, 25)*****
        *****List additional available pins on Model B+*****
    """
    def __init__(self, mode, pins):
        """Set up the devices connected to the pins.
        Give each device a number relating to the
        BCM number of the pin.
        Arguments:
          mode: GPIO.BCM or GPIO.BOARD. See Python RPi.GPIO for details.
          pins (dict): Keys = the pin numbers, values = GPIO.IN or GPIO.OUT
        """
        self.mode = mode
        self.pins = pins

    def set_output(self, pin, output):
        """For pins set to GPIO.OUT, change their output from low to high.
        """
        GPIO.output(pin, output)

    def read_input(self, pin):
        """Read the value of a pin
        Arguments:
          pin (int): the number of the GPIO pin
        """
        return GPIO.input(pin)

    def setup_pins(self, mode, pins):
        """Set up pins for input or output.
        Resets all pins before anything is set.
        Arguments:
          mode       : Either GPIO.BCM or GPIO.BOARD
          pins (dict): A dictionary of pin numbers and pin setup,
                      (GPIO.IN or GPIO.OUT.
        """
        GPIO.cleanup()
        GPIO.setmode(mode)
        for pin in pins.keys():
            GPIO.setup(pin, pins[pin])

    def cleanup(self):
        GPIO.cleanup()


class Watcher(threading.Thread):
    """Class to start a loop where if motion is sensed, lights will
    blink and sounds will play if speakers are connected.
    Depends on a PumpkinGPIO object.
    """
    def __init__(self, controller, stop):
        threading.Thread.__init__(self)
        self.controller = controller
        self.stoprequest = stop

    def run(self):
        time.sleep(10)
        GPIO.output(PIR_POWER, GPIO.HIGH)

        while not self.stoprequest.is_set():
            movement = GPIO.input(4)

            try:
                if movement is True:
                    print "I sense movement!!!"
                    self.controller.play_sound()
                    self.controller.multi_blibnk([23, 24], 1, 8)
                    time.sleep(10)
                else:
                    print ".",
                    time.sleep(5)

            except KeyboardInterrupt:
                break

        GPIO.cleanup()
        exit()


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


rightblnk_M = ((RIGHT_LED,), MEDIUM, 0)
left_blnk_M = ([LEFT_LED], MEDIUM, 0)
rightblnk_F = ((RIGHT_LED,), FAST, 0)
left_blnk_F = ([LEFT_LED], FAST, 0)
dl_blnk_F = ((LEFT_LED, RIGHT_LED), FAST, FAST)
dl_blnk_S = ((LEFT_LED, RIGHT_LED), SLOW, SLOW)

pattern01 = (rightblnk_M, left_blnk_M, rightblnk_M,
             left_blnk_M, dl_blnk_F, dl_blnk_F,
             dl_blnk_F, dl_blnk_F
             )


pattern02 = (dl_blnk_F, rightblnk_F, left_blnk_F, dl_blnk_F)

pattern02 = (dl_blnk_F,)
