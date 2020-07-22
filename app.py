#!/usr/bin/env python
from importlib import import_module
import os
from wifi import Cell, Scheme
from flask import Flask, render_template, Response, request, jsonify, make_response

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
def update_wifi():
    if request.method == 'GET':
        connections = Cell.all('wlan0')
        ssids = []
        for connection in connections:
            ssids.append(connection.ssid)
            print(connection)
        return jsonify(data=ssids)

    elif request.method == 'POST':
        body = request.get_json()

        ssid = body["ssid"]
        password = body["password"]

        connections = Cell.all('wlan0')

        cell = None

        for connection in connections:
            print(connection.ssid)
            if connection.ssid == ssid:
                cell = connection
                break;

        if cell == None:
            return make_response(jsonify(message="Could not find ssid"), 400)

        scheme = Scheme.for_cell('wlan0', 'home', cell, password)
        scheme.activate()
        return

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
