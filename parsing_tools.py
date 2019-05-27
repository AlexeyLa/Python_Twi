# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:46:00 2019

@author: a.lantsov
"""

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup as bs
import re
#import sys
import tweepy
#import urllib2

def get_twitter_link(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    ms = bs(response.read())
    table = ms.find_all(lambda tag: bool(tag.get('href')) and 'twitter.com' in tag.get('href'))
    if (len(table)!=0):
        return table[0].get('href')
    else:
        print('None found')
        return None
    
def get_twitter_link_test(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    ms = bs(response.read())
    table = ms.find_all(lambda tag: bool(tag.get('href')) and 'twitter.com' in tag.get('href'))
    if (len(table)!=0):
        print('main page twitter')
        return table[0].get('href')
    else:
        if url[-1]!='/':
            url+='/'
        req = urllib.request.Request(url + 'contact')
        response = urllib.request.urlopen(req)
        ms = bs(response.read())
        table = ms.find_all(lambda tag: bool(tag.get('href')) and 'twitter.com' in tag.get('href'))
        if (len(table)!=0):
            print("contact twitter")
            return table[0].get('href')
        else:
            return None

def get_correct_link(url):    
    start = re.search(r'twitter.com/',url).start()   
    if (re.search(r'\?',url)):
        stop = re.search(r'\?',url).start()
        corrected_url = 'https://' + url[start:stop]
    else:
        corrected_url = 'https://' + url[start:] 
    return corrected_url

def ref2acc(ref):
    if (ref!=None) and ((len(ref.split('twitter.com/',1))!=1)):
        tw_acc  = ref.split('twitter.com/',1)
        if len(tw_acc)!=1:
            result = tw_acc[1]
            result = result.replace('@','')
            return re.split('[!#$/?]', result)[0]
    else: return None
        
def load_and_save_tweets(api, username, tweets_count, folder):
    uploaded = open(folder + username + '.txt','w')
    print('done')
    print(username)
    try:    
        tweets_list = []
        for tweet_info in api.user_timeline(screen_name=username, tweet_mode = 'extended', count=tweets_count):
            if ('retweeted_status' in dir(tweet_info)):
                tweet=tweet_info.retweeted_status.full_text
            else:
                tweet=tweet_info.full_text
            tweet = (tweet.split('https://',1)[0]).replace('\n','')
            tweets_list.append(tweet + '\n')
        for i in tweets_list:
            mystring = re.sub(r'[^\x00-\x7f]',r'', i) 
            uploaded.write(mystring)
    except tweepy.TweepError:
        uploaded.close()
        
#def check_status(username):
#    url = 'http://api.twitter.com/1/users/show.json?id=%s'
#    try:
#        request = urllib2.urlopen(url)
#        status = request.code
#        data = request.read()
#    except urllib2.HTTPError, e:
#        status = e.code
#    data = e.read()
    
    
    
    
    