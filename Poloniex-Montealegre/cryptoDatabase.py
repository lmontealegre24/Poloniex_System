# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:07:06 2018

@author: lmontealegre
"""
#%%
import requests

class Coin(object):
    
    def __init__(self,   
            id               = "",
		     crypto           = "",
		     market           = "",
		     lowestAsk        = "", 
		     low24hr          = "", 
		     highestBid       = "", 
		     high24hr         = "", 
		     last             = "",
		     isFrozen         = ""):
        
        self.id            = id
        self.crypto        = crypto
        self.market        = market		
        self.lowestAsk     = lowestAsk
        self.low24hr       = low24hr
        self.highestBid    = highestBid
        self.high24hr      = high24hr
        self.last          = last
        self.isFrozen      = isFrozen
          
    def __repr__(self):
        return "Coin"
    
    def __str__(self):
        s = len(self.crypto)+7
        output=  "Coin: %s | Last Price: %s %s"  % (self.crypto, self.last, self.market.lower())		
        output+= "\n%s| Percent Change: %f%% %s" % (' '*s, float(self.percentChange)*100, self.market.lower())
        output+= "\n%s| ---"                     % (' '*s)
        output+= "\n%s| Low 24hr: %s %s"         % (' '*s, self.low24hr, self.market.lower())
        output+= "\n%s| High 24hr: %s %s"        % (' '*s, self.high24hr, self.market.lower())
        output+= "\n%s| ---"                     % (' '*s)
        return output


class Crypto(object):
    
	def __init__(self):
		self.pairs= self.load()

	def load(self):
		data= requests.get('https://poloniex.com/public?command=returnTicker')
		data= data.json()
		pairs= {}
		for pair in data:
			ids= pair.split('_')
			info= data[pair]
			pairs[(ids[0], ids[1])]= info
		return pairs

	def refresh(self):
		self.pairs= self.load()

	def grabPair(self, market, crypto):

		crypto, market= crypto.upper(), market.upper()
		pair= (market, crypto)
		
		try: 
			info= self.pairs[pair]
		except:
			print("Error: %s is not on the %s market" % (crypto, market))
			return

		return Coin(info['id'],
				 crypto,
				 market,
				 info['lowestAsk'],
				 info['low24hr'],
				 info['highestBid'],
				 info['high24hr'],
				 info['last'],
				 info['isFrozen'])
