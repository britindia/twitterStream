#! /usr/bin/env python
# Command to start Notebook: jupyter notebook --ip=127.0.0.1
##################################################################################################################################
# This python module use twitter API to get the tweets for a hashtag entered by user.
# This program first authenticate using twitter developer account.
# This Program then call Twitter developer trends_place api  to get top 4 ternding hashtags in usage
# Program then build a html page (embedTweet.html) dynamically 
# Program then start Streaming live tweets using tweepy.StreamListener class
# Program then get userid and tweet id from streaming class  
# Program then dynamically build tweet URL 
# Program then create EMBEDDED tweet using Twitter API statuses/oembed with tweet url as input
# Program finally render first 10 tweets 
# This program is called from @app.route function in main_flask.py wrapper
# 			Input: Twitter developer tweepy.StreamListener class api
# 			Output: embedTweet.html file
##################################################################################################################################

import tweepy
#from tweepy import StreamListener
# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
import time
import os
from datetime import datetime
import requests
import sys
import json

# Create developer account and get below credentials
consumer_key="xxxxxxxxxxxx"
consumer_secret="xxxxxxxxxxxx"
access_key="xxxxxxxxxxxx"
access_secret="xxxxxxxxxxxx"
  
# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=4):
        self.start_time = time.time()
        self.limit = time_limit
        self.embedded_tweet=[]
#         self.tweet_count=0
        super(MyStreamListener, self).__init__()
        
    def on_status(self, status):
        
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")
        print(status.id_str)
#         print("is_retweet: {}".format(is_retweet))

        # check if text has been truncated
        if hasattr(status,"extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",","\n"]
#         remove_characters = [","]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")
          
#           retrive user_id and tweet_id to form tweet url
        url1= "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
        # print(url1)
                
#           create EMBEDDED tweet using Twitter API statuses/oembed with tweet url as input
        oembedd_url="https://publish.twitter.com/oembed?url=" + url1
        res = requests.get(oembedd_url)
        # print(res.json()["html"])
        
#           use API json response (res.json()) to retrive and save embedded HTML snippet into a list
        if is_retweet==False:
            self.embedded_tweet.append(res.json()["html"])
            tweet_list.append(res.json()["html"])
        
        if time.time() - self.start_time > self.limit:
            return False
            
            
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()
        
def top_hashtags():
	tags = api.trends_place(23424977) # 23424977 Corresponds to the Yahoo ID for USA. Change this to the location that you require.
# 	print("tags_list: {}".format(tags[0]["trends"]))

#       load json into a dictionary
	tags_dict = tags[0]["trends"]

#       create a empty list to collect hashtags
	hastag_list=[]  
#       iterate through tags_dict and collect hashtags
	for i in tags_dict:
	    
		hastag_list.append(i["name"])
	print("hastag_list: {}".format(hastag_list[:4]))
	return(hastag_list[:4])



if __name__ == "__main__":
    print("Start Time:{}".format(time.time()))
    args = sys.argv[1:]
    print("hashtag: {}".format(args[0]))
    # complete authorization and initialize API endpoint
    tweet_list=[]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print("Auth successfull")
    # initialize stream
    streamListener = MyStreamListener()
    print("streamListener successfull")
    top_hastag_list=top_hashtags()
    with open("templates/embedTweet.html", "w", encoding='utf-8') as f:
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
               f.write("%s\n" % '<b>Recent tweets for <u>{{handle}} </u></b>')
    tweet_count=0
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    print("stream object created successfully")
    tags = [args[0]]
    print("Current tag: {}".format(tags))
    stream.filter(track=tags)
    # print("tweet_list: {}".format(tweet_list))
    with open("templates/embedTweet.html", "a", encoding='utf-8') as f:
          while (tweet_count <10 and tweet_count< len(tweet_list)):
                f.write("%s\n" % tweet_list[tweet_count])
                print("List Output")
                print(tweet_list[tweet_count])
                tweet_count += 1
    print("last step successfull")
    print("End Time:{}".format(time.time()))
