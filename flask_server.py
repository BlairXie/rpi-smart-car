#!/usr/bin/env python3
# --coding: utf-8 --
from flask import Flask, abort, redirect, url_for, render_template
from flask import Response,request
from flask import stream_with_context
from camera_pi_android import Camera

#import from other files
from multiprocessing import Process
from ultrasonic import *
from motor import *
app = Flask(__name__)


stream_headers = {
        'Age': 0,
        'Cache-Control': 'no-cache, private',
        'Pragma': 'no-cache',
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
}

@app.route('/',methods=["post","get"])
def show_index():
    try:
        button = request.form["button"]
        if button:
            print(button)
    except:
       None
    return render_template('flask_server.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        wrapped_frame = (b'--frame\r\n' +
                         b'Content-Type: image/jpeg\r\n' +
                         bytes('Content-Length: {}\r\n\r\n'.format(len(frame)),encoding='UTF-8')
                         + frame + b'\r\n')
        yield wrapped_frame


@app.route('/video_feed')
def video_feed():
    global headers
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype=stream_headers['Content-Type'],
                    headers=stream_headers,
                    status=200)

if __name__=='__main__':
    p1 = Process(target=call_forward_avoid_obstacle)
    p1.start()
    app.run(host='0.0.0.0',port=80,debug=False,processes=1,threaded=True)#开启进程支持和线程支持
