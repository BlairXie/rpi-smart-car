#!/usr/bin/env python3
from flask import Flask, abort, redirect, url_for, render_template
from flask import Response
from camera_pi import Camera
# import ultrasonic
app = Flask(__name__)

@app.route('/')
def show_index():
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

@app.route('/<direction>')
def button(direction):

    return redirect(url_for('show_index'))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000, debug=True, threaded=True)
