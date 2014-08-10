#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests
import shutil

import flask
import flask.views
app = flask.Flask(__name__)
from flask import render_template, Response, request
from flask import send_from_directory, redirect

app.config['APK_DIR'] = 'upload'

STATIC_URL_PREFIX = "http://173.255.205.164/static/"

def launcher_details():
    arr = []
    for folder in os.listdir('upload'):
        d ={}
        d['launcher_name'] = "_".join(folder.split('_')[:-1])
        d['launcher_apk'] = STATIC_URL_PREFIX + folder +'/launcher.apk' 
        d['launcher_version'] = folder.split('_')[-1]
        arr.append(d)
    return arr

@app.route('/api')
def api():
    arr = launcher_details()
    return json.dumps(arr)

@app.route('/api/<launcher_name>')
def api_(launcher_name):
    arr = launcher_details()
    d = [i for i in arr if i['launcher_name'] == launcher_name][0]
    return json.dumps(d)

@app.route('/')
def main():
    arr = launcher_details()
    return flask.render_template('index.html',arr=arr)


@app.route('/upload_apk', methods=['POST'])
def upload_apk():
    launcher_name = request.form['launcher_name']
    launcher_version = request.form['launcher_version']
    launcher_apk = request.files['launcher_apk']

    directory = "%s/%s_%s/"%(app.config['APK_DIR'],launcher_name,launcher_version)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    directory = directory + os.path.sep
    fle = open(directory + 'launcher.apk', "w+")
    fle.write(launcher_apk.read())
    fle.close()
    return "Launcher uploaded successfully"

@app.route('/delete/<launcher_name>')
def delete(launcher_name):
    try:
        shutil.rmtree('upload/' + launcher_name)
        msg = "Your launcher has been successfully removed."
    except:
        msg = 'unable to find this launcher'

    return msg


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)

