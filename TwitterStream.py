import tweepy
#from tweepy import StreamListener
# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
import time
import os

consumer_key="aaaa"
consumer_secret="bbb"
access_key="2339533255-ccc"
access_secret="dddd"
output_file="/Users/brijeshtyagi/Desktop/002MIsc/GCP/twitter.txt"

# auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
# auth.set_access_token(access_token,access_token_secret)
# api=tweepy.API(auth)
# tweets = api.home_timeline()

# class StdOutListener(StreamListener):
# 
#   def on_status(self, status):
#       print (status.author.screen_name, status.created_at, status.text)
#   
#   def on_data(self,data):
#     try:
#       print data
#       print("In data")	AS
#       savefile=open("/Users/brijeshtyagi/Desktop/002MIsc/GCP/twitter.txt","a")
#       savefile.write(data)
#       savefile.write('\n')
#       savefile.close()
#       return true
#     except BaseException,e:
#       print 'Failed on Data',str(e)
#       time.sleep(5)
#       
#   def on_error(self,status_code):
#       print(status_code)
#       print >> sys.stderr, 'Encountered error with status code:', status_code
#       return True # Don't kill the stream
#        
# if __name__ =='__main__':
#   print 'Start main'
#   os.remove(output_file)
#   l=StdOutListener()
#   try:
#    auth=OAuthHandler(consumer_key,consumer_secret)
#    auth.set_access_token(access_token,access_token_secret)
#    print("set_access_token Created")
#   except tweep.TweepError:
#    print 'Error! Failed to get request token.'
#   api=tweepy.API(auth)
# #  stream=tweepy.Stream(auth,l)
# #  stream=Stream(auth=api.auth,listener=l)
#   api=tweepy.API(auth)
#   tweets = api.home_timeline()
#   for tweet in tweets:
#       savefile=open(output_file,"a")
#       savefile.write(tweet.id_str.encode("utf-8") +"-"+ tweet.text.encode("utf-8"))
#       savefile.write('\n')
#       savefile.close()
#   print("Reached End")
  
# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

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
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")

        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    with open("out.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
    tags = ["@AAPL"]
    stream.filter(track=tags)
