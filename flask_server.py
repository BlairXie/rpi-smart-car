#!/usr/bin/env python3
from flask import Flask, abort, redirect, url_for, render_template
from flask import Response,request
from camera_pi import Camera

#import from other files
from multiprocessing import Process
from ultrasonic import *
from motor import *
app = Flask(__name__)

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
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def motor_process():
    try:
        while True:
                dist = distance()
                print("Measured Distance = {:.2f} cm".format(dist))
                time.sleep(0.05)

            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

if __name__=='__main__':
    p1 = Process(target=call_forward_avoid_obstacle)
    p1.start()
    app.run(host='0.0.0.0',port=80,debug=None,processes=1,threaded=True)#开启进程支持和线程支持
