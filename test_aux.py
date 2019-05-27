# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:26:37 2019

@author: a.lantsov
"""

import sys
sys.path.insert(0,'C:\\Users\\a.lantsov\\Desktop\\PYTHON\\Twitter_data')
import parsing_tools
import twitter_credentials

acc = twitter_credentials.crds()
print(acc.consumer_key)

ar = {}

rt = '@Name'
rt_list = [1,2,3,4,5]

ar[rt] = rt_list

folder = 'C:/Users/a.lantsov/Desktop/PYTHON/Acquired_data/'

tw_count = 1000
i = 165
#for i in range(0, 10):
for i in range(163,169):
    parsing_tools.load_and_save_tweets(api, twitter_acc[i], tw_count, folder)
    

a = [1,2,3,4,5,5]
b = [5,5,5,5,6,7,8]
print(a+b)
c = (a+b).sort
print(c)