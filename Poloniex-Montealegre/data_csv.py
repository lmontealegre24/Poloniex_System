# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:06:08 2018

@author: lmontealegre
"""
#%%
from timeseries_data import TimeSeries

analysis = TimeSeries()

# Create list of all coins you are looking to collect data from
crypto_pairs= ['BCH', 'XRP','ETH']

for coins in crypto_pairs:
    pair        = ('BTC', coins)	 
    interval    = 300               # seconds
    start       = '05/20/2018'	     # month/day/year
    end         = '06/03/2018'
    
    # Grab time series data, then turn into dataframe through CollectData function
    analysis.collectData(pair, interval, start, end)
    
    # Show dataframe with parameters
    analysis.show()
    save_as= coins + ".csv"
    
    # Export dataframe to csv
    analysis.toCSV(save_as)