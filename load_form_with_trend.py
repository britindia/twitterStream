#! /usr/bin/env python
# Command to start Notebook: jupyter notebook --ip=127.0.0.1
##################################################################################################################################
# This python module will get currently trending hashtags in USA and dynamically create initial html page.
# This program is called from @app.before_request function in main_flask.py wrapper
# 			Input: Twitter developer trends_place api
# 			Output: render_form.html
##################################################################################################################################
import tweepy
import time
import os
from datetime import datetime
import requests
import sys
import json

consumer_key="BOWnxmDCHYliAI9Zd7YC8UhJm"
consumer_secret="DEakCdZZtE1WkaxN8ixHhYcDNFkMAGjZDeeK7AdWZTP43KZbLg"
access_key="2339533255-NgFpjeUf2Cs8xD14gjeMen8iPJNI2YVEklUOT1n"
access_secret="HLs5BirdhWoeEJC5whOS3ufJw4Yf6mXInFZLRAn9HN1gc"
output_file="/Users/brijeshtyagi/Desktop/002MIsc/GCP/twitter_" + datetime.today().strftime('%Y-%m-%d') + ".txt"

def top_hashtags():
	tags = api.trends_place(23424977) # 23424977 Corresponds to the Yahoo ID for USA. Change this to the location that you require.

#       load json into a dictionary
	tags_dict = tags[0]["trends"]

#       create a empty list to collect hashtags
	hastag_list=[]  
	for i in tags_dict:
	    
		hastag_list.append(i["name"])
	print("hastag_list: {}".format(hastag_list[:4]))
	return(hastag_list[:4])
	
if __name__ == "__main__":
    print("Start Time:{}".format(time.time()))
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print("Auth successfull")
    top_hastag_list=top_hashtags()
    print("top_hastag_list: {}".format(top_hastag_list))
    with open("templates/render_form.html", "w", encoding='utf-8') as f:
               f.write("%s\n" % '<body style="background-color:steelblue;">')
               f.write("%s\n" % '<h2>Twitter Live Stream</h2>')
               f.write("%s\n" % '<style>')
               f.write("%s\n" % '    .button {')
               f.write("%s\n" % '  border: none;')
               f.write("%s\n" % '  color: black;')
               f.write("%s\n" % '  padding: 5px 10px;')
               f.write("%s\n" % '  text-align: center;')
               f.write("%s\n" % '  text-decoration: none;')
               f.write("%s\n" % '  display: inline-block;')
               f.write("%s\n" % '  font-size: 12px;')
               f.write("%s\n" % '  margin: 2px 1px;')
               f.write("%s\n" % '  cursor: pointer;')
               f.write("%s\n" % '}')
               f.write("%s\n" % '.button1 {background-color: #8B4513;} /* Green */')
               f.write("%s\n" % '</style>')
               f.write("%s\n" % '<form action="/data" method = "POST">')
               f.write("%s\n" % '    <p>Enter Tag <input type = "text" name = "Tag" /> <button class="button button1">Submit</button> </p>')
               f.write("%s\n" % 'Currently trending in USA:  <b style="color:blue;"> {}, {}, {}, {}</b>'.format(top_hastag_list[0],top_hastag_list[1],top_hastag_list[2],top_hastag_list[3])) 
               f.write("%s\n" % '    <marquee behavior="scroll" direction="right">After Submit, please stay put while we collect your tweets!</marquee>')
               f.write("%s\n" % '</form>')
               f.write("%s\n" % '</body>')
#                f.write("%s\n" % '<b>Recent tweets for <u>{{handle}} </u></b>')
    print("last step successfull")
    print("End Time:{}".format(time.time()))