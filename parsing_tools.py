# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:46:00 2019

@author: a.lantsov
"""

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup as bs
import re

def get_twitter_link(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    ms = bs(response.read())
    table = ms.find_all(lambda tag: bool(tag.get('href')) and 'twitter.com' in tag.get('href'))
    if (len(table)!=0):
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

#def get_tweets(url):
    
    
    