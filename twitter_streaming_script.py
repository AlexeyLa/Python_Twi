# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:29:32 2019

@author: a.lantsov
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import twitter_credentials

acc = twitter_credentials.crds()

folder = 'C:/Users/a.lantsov/Desktop/PYTHON/'

save_file = folder + 'test.txt'

class listener(StreamListener):
    def on_data(self, data):
        with open(save_file,'a') as tf:
            tf.write(data)
        return(True)
    def on_error(self, status):
        print(status)

auth = OAuthHandler(acc.consumer_key, acc.consumer_secret)
auth.set_access_token(acc.access_token_key, acc.access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Venezuela"])

