#!/usr/bin/env python3
from flask import Flask
from flask import abort, redirect, url_for, render_template
# import ultrasonic
app = Flask(__name__)

@app.route('/')
def show_index():
  return render_template('flask_server.html')

@app.route('/<direction>')
def button(direction):

    return redirect(url_for('show_index'))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
