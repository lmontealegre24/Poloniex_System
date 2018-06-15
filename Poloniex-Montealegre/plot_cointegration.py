# -*- coding: utf-8 -*-
"""

@author: lmontealegre
"""
#%%
import os
import itertools as it

coins = [file for file in os.listdir() if ".csv" in file]

coin_dict = {}

for coin in coins:
    coin_dict[coin.split(".")[0]] = pd.read_csv(coin)['VWAP']
    


correlations = []

for pair in list(it.combinations(list(coin_dict.keys()),2)):
    s0 = coin_dict[pair[0]]
    s1 = coin_dict[pair[1]]
    
    data = pd.DataFrame()
    data['s0'] = s0
    data['s1'] = s1
    
    # print(pair, data.corr().values[0,1])
    correlations.append([pair, data.corr().values[0,1]])
    

correlations = sorted(correlations, key = lambda x:-x[1])
_=[print(item) for item in correlations]

from cointegration import coint

print()

for i in correlations[:]:
    s0 = coin_dict[i[0][0]]
    s1 = coin_dict[i[0][1]]
    
    data = pd.DataFrame()
    data['s0'] = s0
    data['s1'] = s1
    print(i)
    res = coint(data.dropna(), print_test=True)
    print(res.v_norm)
    
    w = res.v_norm.iloc[0][1]
    
    fig, ax = plt.subplots(2,figsize=(15,10), gridspec_kw={'hspace':0})
    ax0 = ax[0].twinx()
    data['s1'] = s1

    
