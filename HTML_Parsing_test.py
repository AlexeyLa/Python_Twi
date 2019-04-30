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
    twitter_list.append(parsing_tools.get_twitter_link(links_list[k]))

# calculate amount of incorrectly processed entitites
    
counter = [counter+1 for i in twitter_list if type(i) is str]
efficiency = len(counter)/len(twitter_list)
print('efficiency: ', efficiency)

# get list of indices fith fault results

#indices = []
indices = [i for i,v in enumerate(twitter_list) if type(v) != str]

# correct twitter links

twitter_list_correct = []
counter = 0
for m in twitter_list:
    print(counter)
    if (m==None):
        twitter_list_correct.append(m)
    else:
        print(type(m))
        twitter_list_correct.append(parsing_tools.get_correct_link(m))
        print("correct")
    counter+=1   
        