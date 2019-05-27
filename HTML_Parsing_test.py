# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:36:07 2019

@author: a.lantsov
"""

# parse html url
import sys
import os

path = 'C:\\Users\\a.lantsov\\Desktop\\PYTHON\\'
sys.path.insert(0,path + 'Twitter_data\\')
sys.path.insert(0,path + 'Python_Twi\\')
os.chdir(path + 'Python_Twi\\')

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup as bs
#import re
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
twitter_acc = [i for i in twitter_acc if i is not None]

# create txt files with text from tweets

import tweepy
from tweepy import OAuthHandler
import twitter_credentials

acc = twitter_credentials.crds()

consumer_key = acc.consumer_key
consumer_secret = acc.consumer_secret
access_token_key = acc.access_token_key
access_token_secret = acc.access_token_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

folder = 'C:/Users/a.lantsov/Desktop/PYTHON/Acquired_data/'

tw_count = 1000
#for i in range(0, 10):
count = 0
for i in twitter_acc:
    count+=1
    print(count)
    parsing_tools.load_and_save_tweets(api, i, tw_count, folder)
    
# get list of twits from file

user_twits = {}
for j in twitter_acc:
    loaded = open(folder + j + '.txt','r')
    f = loaded.readlines()
    twits = []
    for i in f:
        twits.append(i)
    loaded.close()
    user_twits[j] = twits

# start Named Entity Recognition with obtained twits (NLTK + SpaCy)

import nltk
nltk.download()
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

interim = preprocess(user_twits[1])

analysis_res = []
for i in user_twits:
    analysis_res.append(preprocess(i))

# let's use spacy which was trained upon OntoNotes5 corpus

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

full_analysis = []
full_labels = []
labels = []
items = []

user_analysis = {}

for key, value in user_twits.items(): 
    geotag_list = []
    for i in value:
        doc = nlp(i)
        for X in doc.ents:
            if (X.label_ == 'GPE'):
                geotag_list.append(X.text)
    user_analysis[key] = geotag_list
                
ven_counter = {}

for key, value in user_twits.items():
    counter = 0
    for i in value:
        if 'Venezuela' in i:
            counter+=1               
    ven_counter[key] = counter

# sort dictionary
    
import operator

sorted_x = sorted(ven_counter.items(), key = operator.itemgetter(1))
                    
#    full_analysis.append([(X.text, X.label_) for X in doc.ents])
#    full_labels.append([X.label_ for X in doc.ents])
#    items+=[X.text for X in doc.ents]
#    labels+=[X.label_ for X in doc.ents]
#result_labels = Counter(labels).most_common(10)
#result_items = Counter(items).most_common(10)

# analyzed full set of twitter accounts


