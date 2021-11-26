#! /usr/bin/env python3
####!/usr/bin/python
# Output @ http://localhost:5000
##################################################################################################################################
# This flask wrapper is used to create a dynamic html application.
# This application receive value of hashtag as input and use the developer twitter API to render first 10 tweets.
# Application also list top 4 trending hashtags in USA.
# 			Input:  load_form_with_trend.py - python Module
#                   TwitterStream.py - python Module 
# 			Output: render_form.html
#                   embedTweet.html
##################################################################################################################################


from flask import Flask,render_template,request
import os
import csv
import sys
import subprocess
import time

app = Flask(__name__)

# Get new out.html everytime Submit button is clicked
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.before_request
def before_request_func():
    print("before_request is running!")
    subprocess.call([sys.executable,"load_form_with_trend.py"])
    
@app.route('/')
def form():
    return render_template('render_form.html')
    
@app.route('/data/', methods = ['POST', 'GET'])
def data():
#     time.sleep(5)
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        handle=form_data["Tag"]
        print('Sub-process Started')
#         subprocess.check_output([sys.executable,"TwitterStream.py"])
        subprocess.call([sys.executable,"TwitterStream.py",handle,'no'])
        print('Sub-process Finished')
        return render_template('embedTweet.html', **locals())
app.run(host='localhost', port=5000)