#!/usr/bin/env python

# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import StateManager

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def vehicle_data():     
     global gState
     return render_template('vehicle_controls.html', IP=gState.local_IP(), accelerator=gState.get_accelerator(), angle=gState.get_angle())

@app.route('/stop', methods=['POST'])
def stop():
     #Stop the automatic updates
     flash('Updates halted.')
     session['updates_paused'] = True
     global gState
     gState.pause()
     return redirect(url_for('vehicle_data'))

@app.route('/single', methods=['POST'])
def single():
     #make a global socket
     flash('Single packet sent.')
     global gState
     gState.update_once()
     return redirect(url_for('vehicle_data'))

@app.route('/start', methods=['POST'])
def start():
     #make a global socket
     flash('Updates resumed.')
     session.pop('updates_paused', None)
     global gState
     gState.resume()
     return redirect(url_for('vehicle_data'))

@app.route('/steering', methods=['POST'])
def update_steering_wheel():
     angle = float(request.form['angle'])
     print "New Steering Wheel Angle: " + str(angle)
     flash('Steering Wheel Angle set to ' + str(angle))
     global gState
     gState.update_angle(angle)
     return redirect(url_for('vehicle_data'))

@app.route('/accelerator', methods=['POST'])
def update_accelerator():
     accelerator = float(request.form['accelerator'])
     if (accelerator >= 0) and (accelerator <= 100):
          print "New Accelerator Position: " + str(accelerator)
          flash('Accelerator Percentage set to ' + str(accelerator))
          global gState
          gState.update_accelerator(accelerator)
     else:
          flash('Accelerator Percentage must be between 0 and 100.')
     return redirect(url_for('vehicle_data'))

if __name__ == '__main__':
     print 'Running Main...'
     
     global gState
     gState = StateManager.StateManager()

     app.run(use_reloader=False)
     
