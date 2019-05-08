# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:36:07 2019

@author: a.lantsov
"""

# parse html url
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import parsing_tools
import pickle

url = 'https://www.house.gov/representatives'
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
web_content = response.read()

my_soup = bs(web_content)

table_x = my_soup.find_all('table')

reps_list = []
links_list = []
states_list = []
party_list = []
try:
    for i in range(0, len(table_x)):
        state_name = table_x[i].find('caption').get_text().lstrip().rstrip()
# parse names and links to representatives
        ref_list = table_x[i].find_all('a')
        party = table_x[i].find_all('td')
        num_delegates = (int)(len(party)/6)
        for i in range(0, num_delegates):
            party_list.append(party[i*6 + 2].get_text().rstrip())           
            links_list.append(party[i*6 + 1].find('a').get('href'))
            reps_list.append(party[i*6 + 1].get_text())
            states_list.append(state_name)
except:
    print("states list is full")
    
data = [[i,j,k] for i,j,k in zip(links_list, party_list, states_list)]   
full_dict = dict(zip(reps_list, data))

# save obtained links list

pickle_out = open("links_list.pickle","wb")
pickle.dump(links_list, pickle_out)
pickle_out.close()

# load links list

pickle_in = open("links_list.pickle","rb")
links_list = pickle.load(pickle_in)

# get twitter links from links list 

counter = 0
twitter_list = []
#for k in range(0,10):
for k in range(0,len(links_list)):
    print(k)
    twitter_list.append(parsing_tools.get_twitter_link_test(links_list[k]))

# calculate amount of incorrectly processed entitites
    
counter = [counter+1 for i in twitter_list if type(i) is str]
efficiency = len(counter)/len(twitter_list)
print('efficiency: ', efficiency)

# get list of indices fith fault results

#indices = []
indices = [i for i,v in enumerate(twitter_list) if type(v) != str]      
    
# save obtained twitter acc list

pickle_out = open("twitter_list.pickle","wb")
pickle.dump(twitter_list, pickle_out)
pickle_out.close()

# load twitter acc list

pickle_in = open("twitter_list.pickle","rb")
twitter_list = pickle.load(pickle_in)

# convert twitter link to accounts
                 
twitter_acc = [parsing_tools.ref2acc(i) for i in twitter_list]

# create txt files with text from tweets

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

tw_count = 50
for i in range(0, 8):
    parsing_tools.load_and_save_tweets(api, twitter_acc[i], tw_count)
    
# get list of twits from file

user_twits = []    
loaded = open(twitter_acc[0][1:] + '.txt','r')
f = loaded.readlines()
for i in f:
    user_twits.append(i)
loaded.close()





