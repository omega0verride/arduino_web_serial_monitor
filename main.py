from flask import Flask, render_template, request, jsonify
import threading
import logging
import serial
import argparse


default_bytes_to_drop = 1000
default_max_output_bytes = 4000

parser = argparse.ArgumentParser(description='Arduino Lan Serial Monitor.')
parser.add_argument('-p', '--port', metavar='PORT', nargs=1, required=True, help='Serial Port Where Arduino Board is Connected.',)
parser.add_argument('-b', '--baud', metavar='BaudRate', help='Serial BaudRate.', nargs=1, type=int, required=True, choices=[300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200])
parser.add_argument('-bd', '--bytedrop', metavar='Number of Bytes', default=default_bytes_to_drop, nargs=1, type=int, help='Number of bytes to remove to Not overload the server. Default: %d' %default_bytes_to_drop)
parser.add_argument('-mb', '--maxbytes', metavar='Number of Bytes', default=default_max_output_bytes, nargs=1, type=int, help='Max bytes that the serial monitor can keep cached. Default: %d' %default_max_output_bytes)
args = parser.parse_args()

port = args.port[0]
baud = args.baud[0]
bytes_to_drop = args.bytedrop
max_output_bytes = args.maxbytes

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
filesDirectory = 'temp'

global serial_return
serial_return = "---Start---\n"

try:
    arduino = serial.Serial(port, baud)
except Exception as e:
    serial_return = str(e)

def readSerial():
    while 1:
        data = arduino.read()

        global serial_return
        try:
            serial_return = serial_return + str(data.decode())
        except:
            serial_return = serial_return + str(data)

        if len(serial_return) > max_output_bytes:
            serial_return = serial_return[bytes_to_drop:len(serial_return)]


@app.route('/send_serial_data/')
def send_serial_data():
    data = str(request.args.get('data', 0, type=str))
    arduino.write(data.encode())
    return jsonify(0)


@app.route('/update_log_status/')
def update_log_status():
    text = []
    for data in serial_return.split('\n'):
        text.append(data)
    return jsonify(text=text)


@app.route('/clearSerialOutput/')
def clearSerialOutput():
    global serial_return
    serial_return = ''
    return jsonify(0)


@app.route('/')
def log():
    return render_template('serial.html', port=port, text=serial_return)


def flaskServer():
    app.run(host='0.0.0.0', port=80, threaded=1)


if __name__ == "__main__":
    flask_Server_process = threading.Thread(target=flaskServer, daemon=True, args=())
    serial_read_Process = threading.Thread(target=readSerial, args=())


    flask_Server_process.setDaemon(serial_read_Process)
    serial_read_Process.start()
    flask_Server_process.start()
    serial_read_Process.join()
