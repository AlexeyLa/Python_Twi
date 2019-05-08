# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:10:00 2018

@author: Alexey
"""

import tweepy
from tweepy import OAuthHandler
import twitter

import re

consumer_key='tuuPxYC2QYqMqCor41TuLlEWV'
consumer_secret='NMeqN2w0KhnkbT4CFk3ef3Oi7SR1NlfLfQV3OnQtUwkd8czam0'
access_token_key='2809175323-8rlwmRgpkYed0E9Lb36V7VxoIlBaULlUyAJtdNA'
access_token_secret='LbwpuZZWpxichjGXJS3TmBYLY2COyofjnb2KyrOj2b02h'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

def load_and_save_tweets(username, tweets_count):
    uploaded = open(username[1:] + '.txt','w')
    tweets_list = []
    for tweet_info in api.user_timeline(screen_name=username, tweet_mode = 'extended', count=tweets_count):
        if ('retweeted_status' in dir(tweet_info)):
            tweet=tweet_info.retweeted_status.full_text
            tweets_list.append(tweet)
        else:
            tweet=tweet_info.full_text
            tweets_list.append(tweet)
    for i in tweets_list:
        uploaded.write(i + '\n')
    uploaded.close()

#for status in tweepy.Cursor(api.home_timeline).items(1):
#    print(status.text)
users = ['@sitovskaya', '@PanShehtman']
tweets_count = 5
#for us in users:
#    print(us)
#    load_and_save_tweets(us, tweets_count)
load_and_save_tweets('@repshimkus', tweets_count)
    


