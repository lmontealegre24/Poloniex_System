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
    
    def refresh(self):
        self.crypto_pairs= self.load()    
    
    def grabPair(self, market, crypto):
        crypto, market= crypto.upper(), market.upper()
        pair= (market, crypto)
        
        try: 
            info= self.crypto_pairs[pair]
        except:
            print("Error: %s is not on the %s market" % (crypto, market))
            return
        
        return Information(info['id'],
				 crypto,
				 market,
				 info['lowestAsk'],
				 info['highestBid'],
				 info['low24hr'],
				 info['high24hr'],
				 info['last'],
				 info['percentChange'],
				 info['baseVolume'],
				 info['quoteVolume'],
				 info['isFrozen'])

class Information(object):
    def __init__(self, id= "", crypto= "", market= "",
		     lowestAsk= "", highestBid= "", low24hr= "", 
		     high24hr= "", last= "", percentChange= "",
            baseVolume= "", quoteVolume= "", isFrozen= ""):
        self.id            = id
        self.crypto        = crypto
        self.market        = market		
        self.lowestAsk     = lowestAsk
        self.highestBid    = highestBid
        self.low24hr       = low24hr
        self.high24hr      = high24hr
        self.last          = last
        self.percentChange = percentChange
        self.baseVolume    = baseVolume		
        self.quoteVolume   = quoteVolume
        self.isFrozen      = isFrozen
    
    def __repr__(self):
        return "Coin"
    
    def __str__(self):
        ob=  "Crypto: %s \nLast Price: %s %s\n"  % (self.crypto, self.last, self.market.lower())		
        ob+= "24hr Percent Change: %f%% %s\n" % (float(self.percentChange)*100, self.market.lower())
        ob+= "Low 24hr: %s %s\n"         % (self.low24hr, self.market.lower())
        ob+= "High 24hr: %s %s\n"        % (self.high24hr, self.market.lower())
        ob+= "Base Volume: %s %s\n"      % (self.baseVolume, self.market.lower())
        ob+= "Quote Volume: %s %s\n"     % (self.quoteVolume, self.crypto.lower())
        return ob
        

    

#%%

test= Orderbook().grabPair('BTC','LTC')
print(test)

