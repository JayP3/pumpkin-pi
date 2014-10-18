from flask import Flask, render_template, request
from pumpkinpi import PumpkinPi, pins
import RPi.GPIO as GPIO


app = Flask(__name__)
pumpkin = PumpkinPi(GPIO.BCM, pins)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blink', methods=['POST'])
def blink_lights():
    print "Blinking Light!!!"
    pumpkin.multi_blink([23, 24], 1, 5)
    return render_template('index.html')


@app.route('/sound', methods=['POST'])
def sound():
    print "Playing Sound"
    pumpkin.play_sound()
    return render_template('index.html')


@app.route('/watch', methods=['POST'])
def watch():
    if request.form['watcher'] == 'Start Watching':
        print "Watching for movement!!!"
        pumpkin.run()
    elif request.form['watcher'] == 'Stop Watching':
        print "Stopping the Watch thread"
        pumpkin.stop()
    else:
        print "Bad request???"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
