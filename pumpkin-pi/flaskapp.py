from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/blink', methods=['POST'])
def blink():
    print "Blinking Light!!!"
    return app.send_static_file('index.html')
    
@app.route('/sound', methods=['POST'])
def sound():
    print "Playing Sound"
    return app.send_static_file('index.html')
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
