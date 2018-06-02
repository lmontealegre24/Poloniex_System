#%%

import requests

class Coin(object):
    
    def __init__(self,   
            id            = "", 
		     Coin          = "",
		     Market        = "",
		     LowestAsk     = "", 
		     Low24hr      = "", 
		     HighestBid    = "", 
		     High24hr      = "", 
		     Last          = "",
		     PercentChange = "", 
		     BaseVolume    = "", 
		     QuoteVolume   = "", 
		     isFrozen      = ""):
        
        self.id            = id
        self.Coin          = Coin
        self.Market        = Market		
        self.LowestAsk     = LowestAsk
        self.Low24hr       = Low24hr
        self.HighestBid    = HighestBid
        self.High24hr      = High24hr
        self.Last          = Last
        self.PercentChange = PercentChange
        self.BaseVolume    = BaseVolume		
        self.QuoteVolume   = QuoteVolume
        self.isFrozen      = isFrozen
          
    def __repr__(self):
        return "Coin"
    
    def __str__(self):
        s = len(self.Coin)+7
        output =  "Coin: %s | Last Price: %s %s"  % (self.Coin, self.Last, self.Market.lower())		
        output += "\n%s| Percent Change: %f%% %s" % (' '*s, float(self.PercentChange)*100, self.Market.lower())
        output += "\n%s| ---"                     % (' '*s)
        output += "\n%s| Low 24hr: %s %s"         % (' '*s, self.Low24hr, self.Market.lower())
        output += "\n%s| High 24hr: %s %s"        % (' '*s, self.High24hr, self.Market.lower())
        output += "\n%s| ---"                     % (' '*s)
        output += "\n%s| Base Volume: %s %s"      % (' '*s, self.BaseVolume, self.Market.lower())
        output += "\n%s| Quote Volume: %s %s"     % (' '*s, self.QuoteVolume, self.Coin.lower())
        return output


class Crypto(object):
    
	def __init__(self):
		self.pairs = self.load()

	def load(self):
		data = requests.get('https://poloniex.com/public?command=returnTicker')
		data = data.json()
		pairs = {}
		for pair in data:
			ids = pair.split('_')
			info = data[pair]
			pairs[(ids[0], ids[1])] = info
		return pairs

	def refresh(self):
		self.pairs = self.load()

	def GrabPair(self, Market, Coin):

		Coin, Market = Coin.upper(), Market.upper()
		pair = (Market, Coin)
		
		try: 
			info = self.pairs[pair]
		except:
			print("Error: %s is not on the %s market" % (Coin, Market))
			return

		return Coin(info['id'],
				 coin,
				 market,
				 info['LowestAsk'],
				 info['Low24hr'],
				 info['HighestBid'],
				 info['High24hr'],
				 info['Last'],
				 info['PercentChange'],
				 info['BaseVolume'],
				 info['QuoteVolume'],
				 info['isFrozen'])
