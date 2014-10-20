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
        self.mode = mode
        self.pins = pins
        self.setup_pins(mode, pins)

    def run(self):
        self.kill_thread.clear()
        t = Watcher(self.kill_thread)
        t.start()

    def stop(self):
        print "Killing the Watcher thread"
        self.kill_thread.set()

    def multi_blink(self, pins, duration, repeat=1):
        for i in range(0, repeat):
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)
            time.sleep(duration)

    def play_sound(self):
        sounddir = os.path.join(os.getcwd(), 'sounds')
        sounds = [x for x in os.listdir(sounddir) if x.lower().endswith('.mp3')]
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

    def cleanup_gpio(self):
        GPIO.cleanup()


class Controller(object):

    def multi_blink(self, pins, duration, repeat=1):
        for i in range(0, repeat):
            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            for pin in pins:
                GPIO.output(pin, GPIO.LOW)
            time.sleep(duration)

    def play_sound(self):
        sounddir = os.path.join(os.getcwd(), 'sounds')
        sounds = [x for x in os.listdir(sounddir) if x.lower().endswith('.mp3')]
        num = random.randint(0, len(sounds) - 1)
        fname = os.path.join('sounds', sounds[num])
        cmd = 'mpg321 -g 500 %s &' % fname
        os.system(cmd)


class Watcher(threading.Thread):
    """Class to start a loop where if motion is sensed, lights will
    blink and sounds will play if speakers are connected.
    Depends on a PumpkinGPIO object.
    """
    def __init__(self, stop):
        threading.Thread.__init__(self)
        self.controller = Controller()
        self.stoprequest = stop

    def run(self):
        print "Starting thread"
        time.sleep(10)
        GPIO.output(PIR_POWER, GPIO.HIGH)

        while not self.stoprequest.is_set():
            movement = GPIO.input(PIR_SENSE)

            try:
                if movement:
                    print "I sense movement!!!"
                    self.controller.play_sound()
                    self.controller.multi_blink([RIGHT_LED, LEFT_LED], 1, 8)
                    time.sleep(10)
                else:
                    print ".",
                    time.sleep(5)

            except KeyboardInterrupt:
                break
        GPIO.output(PIR_POWER, GPIO.LOW)


if __name__ == '__main__':
    pumpkin = PumpkinPi(GPIO.BCM, pins)
    print "Testing LED Lights"
    GPIO.output(RIGHT_LED, GPIO.HIGH)
    GPIO.output(LEFT_LED, GPIO.HIGH)
    raw_input("Press enter to turn lights off")
    GPIO.output(RIGHT_LED, GPIO.LOW)
    GPIO.output(LEFT_LED, GPIO.LOW)
    pumpkin.cleanup_gpio()
