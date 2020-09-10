#!/usr/bin/env python
from importlib import import_module
import os
from wifi import Cell, Scheme
from flask import Flask, render_template, Response, request, jsonify, make_response
from qrscanner import QRScanner
from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/wifi', methods=['GET', 'POST'])
def get_wifi():
    if request.method == 'GET':
        connections = Cell.all('wlan0')
        ssids = []
        for connection in connections:
            ssids.append(connection.ssid)
            print(connection)
        return jsonify(data=ssids)

if __name__ == '__main__':
    #if no wifi connection already
    
    data = QRScanner.startScanning()
    print(data)
    #attempt to connect to access point using data. If not succesfull start scanning for a QR code again.
    
    app.run(host='0.0.0.0', threaded=True)
