# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:51:10 2019

@author: a.lantsov
"""

import re
import parsing_tools

ref = 'https://twitter.com/RepMoBrooks?ref_src=twsrc%5Etfw'
ref = 'https://twitter.com/RepJuanVargas/status/933007562818981888'
ref = 'https://twitter.com/RepByrne'
ref = '//platform.twitter.com'

newres2 = re.sub(r'[^\x00-\x7f]',r'', i) 

res = twitter_acc[5]
tweets_count = 100
username = twitter_acc[7]
uploaded = open('test' + '.txt','w')
tweets_list = []
for tweet_info in api.user_timeline(screen_name=username, tweet_mode = 'extended', count=tweets_count):
    if ('retweeted_status' in dir(tweet_info)):
        tweet=tweet_info.retweeted_status.full_text
    else:
        tweet=tweet_info.full_text
    tweet = (tweet.split('https://',1)[0]).replace('\n','')
    tweets_list.append(tweet + '\n')
for i in tweets_list:
    print(str(tweets_list.index(i)))
    print(i)
    mystring = re.sub(r'[^\x00-\x7f]',r'', i) 
    uploaded.write("count: " + str(tweets_list.index(i)) + " TW: "+ mystring)
uploaded.close()

