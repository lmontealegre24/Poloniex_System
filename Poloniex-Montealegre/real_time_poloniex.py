#%%

import requests


class Orderbook(object):
    def __init__(self):
        self.crypto_pairs=self.load() 
        
    
    def load(self):
        data= requests.get('https://poloniex.com/public?command=returnTicker').json()
        crypto_pairs= {}
        for pair in data:
            ids= pair.split('_')
            info= data[pair]
            crypto_pairs[(ids[0], ids[1])]= info
        return crypto_pairs
    
    
    def grabPair(self, market, crypto):
        crypto, market= crypto.upper(), market.upper()
        pair= (market, crypto)
        
        try: 
            info= self.crypto_pairs[pair]
        except:
            print("Error: %s is not on the %s market" % (crypto, market))
            return
        
    def refresh(self):
        self.crypto_pairs= self.load()

#%%

test= Orderbook()

test= test.load()

all_orderbooks= test.keys()
print("All orderbooks present: \n\n", all_orderbooks)
    
LTC= test[('BTC','LTC')]

print("LTC Orderbook: \n", LTC)
