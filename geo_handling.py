# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:30:11 2019

@author: a.lantsov
"""

import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point

# set the filepath and load in a shapefile

usa = gpd.read_file('./states_21basic/states.shp')

#usa.head()

#usa.plot()

#usa[usa.STATE_ABBR == 'TX'].plot()

#usa[usa.SUB_REGION == 'East North Central'].plot()

def state_plotter(states, us_map=True):
    fig, ax = plt.subplots(figsize = (30,30))
    if us_map:
        if 'HI' in states:
            usa[0:50].plot(ax=ax, alpha = 0.3)
        elif 'AK' in states:
            usa[1:51].plot(ax=ax, alpha = 0.3)
        elif 'AK' and 'HI' in states:
            usa[0:51].plot(ax=ax, alpha = 0.3)
        else:
            usa[1:50].plot(ax=ax, alpha = 0.3)
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax = ax, edgecolor = 'black', linewidth = 1)
    elif us_map == False:
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax = ax, edgecolor = 'white', linewidth = 1)
        
states = [i for i in usa.STATE_ABBR][20:28] 

state_plotter(states, us_map=True)      

#fig, ax = plt.subplots(figsize = (30,30))
#usa[0:51].plot(ax=ax, alpha = 0.3)
#for n in states:
#    usa[usa.STATE_ABBR == f'{n}'].plot(ax=ax, edgecolor = 'black', linewidth = 1)
#state_plotter(states_2, us_map=True)  