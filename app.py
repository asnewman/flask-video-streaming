#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from importlib import import_module
import os
from wifi import Cell, Scheme
from flask import Flask, render_template, Response, request, jsonify, make_response

from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    data.send_email = os.getenv('SEND_EMAIL')

    return render_template('index.html', data=data)


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
    app.run(host='0.0.0.0', threaded=True)
