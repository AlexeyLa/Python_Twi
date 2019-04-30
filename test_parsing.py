# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:31:51 2019

@author: a.lantsov
"""
import parsing_tools

link = 'https://arrington.house.gov'
twitter_link = parsing_tools.get_twitter_link(link)
repaired_link = parsing_tools.get_correct_link(twitter_link)

test_links = []
for i in indices:
    cur_link = twitter_list.append(parsing_tools.get_twitter_link(links_list[i]))
    test_links.append(cur_link)