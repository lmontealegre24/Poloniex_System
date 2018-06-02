#%%
import json
import requests
import time
import csv
import pandas as pd
import datetime as dt

def Unix(strdate):
    date = dt.datetime.strptime(strdate, "%m/%d/%Y")
    return int(time.mktime(date.timetuple()))

def Date(unixdate):
    date = dt.datetime.fromtimestamp(int(unixdate))
    return date.strftime("%m/%d/%Y %H:%M:%S")

def CryptoPairs(pair):
    pairs = ['BTC_RBY', 'USDT_REP', 'BTC_UNITY', 'BTC_PINK', 'BTC_SYS', 'BTC_EMC2', 'BTC_C2', 'BTC_RADS', 'BTC_SC', 'BTC_MAID', 'BTC_BCN', 'BTC_REP', 'BTC_BCY', 'XMR_NXT', 'USDT_ZEC', 'BTC_FCT', 'USDT_ETH', 'USDT_BTC', 'BTC_LBC', 'BTC_DCR', 'USDT_ETC', 'BTC_AMP', 'BTC_XPM', 'BTC_NOBL', 'BTC_NXT', 'BTC_VTC', 'ETH_STEEM', 'XMR_BLK', 'BTC_PASC', 'XMR_ZEC', 'BTC_GRC', 'BTC_NXC', 'BTC_BTCD', 'BTC_BCH', 'BTC_LTC', 'BTC_DASH', 'BTC_NAUT', 'ETH_ZEC', 'BTC_ZEC', 'BTC_BURST', 'BTC_XVC', 'XMR_QORA', 'BTC_BELA', 'BTC_STEEM', 'BTC_ETC', 'BTC_ETH', 'BTC_CURE', 'BTC_HUC', 'BTC_STRAT', 'BTC_LSK', 'BTC_EXP', 'BTC_CLAM', 'ETH_REP', 'BTC_QORA', 'BTC_QTL', 'XMR_DASH', 'USDT_DASH', 'BTC_BLK', 'BTC_XRP', 'USDT_NXT', 'BTC_NEOS', 'BTC_QBK', 'BTC_BTS', 'BTC_DOGE', 'XMR_BBR', 'BTC_SBD', 'BTC_XCP', 'USDT_LTC', 'BTC_BTM', 'USDT_XMR', 'ETH_LSK', 'BTC_OMNI', 'BTC_NAV', 'BTC_VOX', 'BTC_XBC', 'BTC_DGB', 'BTC_NOTE', 'XMR_BTCD', 'BTC_BITS', 'BTC_VRC', 'BTC_RIC', 'XMR_MAID', 'BTC_XMG', 'BTC_STR', 'BTC_POT', 'BTC_BBR', 'BTC_XMR', 'BTC_SJCX', 'BTC_VIA', 'BTC_XEM', 'BTC_NMC', 'BTC_SDC', 'ETH_ETC', 'XMR_LTC', 'BTC_ARDR', 'BTC_HZ', 'BTC_FLO', 'USDT_XRP', 'BTC_GAME', 'BTC_PPC', 'BTC_FLDC', 'XMR_BCN', 'BTC_MYR', 'USDT_STR', 'BTC_NSR', 'BTC_IOC']
    if '%s_%s' % (pair[0], pair[1]) not in pairs:
        print("Error: Must pick a trading pair on Poloniex")
        return False
    return True

def TimeInterval(interval):
    intervals = [300,900,1800,7200,14400,86400]
    if interval not in intervals:
        print("Error: You must choose a time interval displayed on Poloniex: %s" % \
        (str([300,900,1800,7200,14400,86400]).strip("[]")))
        return False
    return True

def Dates(start,end):
    start = dt.datetime.strptime(start, "%m/%d/%Y")
    end = dt.datetime.strptime(end, "%m/%d/%Y")
    if (start>end):
        print("Error: Pick a date that begins before end date")
        return False
    if (end-start).days > 31:
        print("Error: Must choose data interval less than a 31 days (edit for longer)")
        return False
    return True

def URL(pair, interval, start, end):
    base = 'https://poloniex.com/public?command=returnChartData&currencyPair='
    return '%s%s_%s&start=%s&end=%s&period=%s' % \
	(base, pair[0], pair[1], Unix(start), Unix(end), interval)

class TimeSeries(object):
    
    def _init_(self):
        self.empty=True
        self.data=None
        self.pair=("None","None")
        self.interval="None"
        self.start="None"
        self.end="None"
    
    def show(self):
        if self.empty:
            print("No data..")
        else:
            print("Crypto Pair: ('%s', '%s')" % (self.pair[0], self.pair[1]))
            print("Interval: %s" % (self.interval))
            print("Start Date: %s" % (self.start))
            print("End Date: %s" % (self.end))
            print("\n", self.data)
    
    def CollectData(self,pair,interval,start,end):
        if not CryptoPairs(pair):
            return
        if not TimeInterval(interval):
            return
        if not Dates(start,end):
            return
        
        url=URL(pair,interval,start,end)
        datapoints=requests.get(url)
        datapoints=datapoints.json()
        
        headers= ['date', 'open', 'low', 'high', 'close', 'weightedAverage', 'volume', 'quoteVolume']
        data=[]
        for points in datapoints:
            row=[]
            for item in headers:
                if item == 'date':
                    row.append(Date(points[item]))
                else:
                    row.append(points[item])
            data.append(row)
            
        df=pd.DataFrame(data, columns = headers)
        df.index=pd.to_datetime(df["date"])
        df.drop("date", axis =1, inplace=True)
        
        self.data=      df
        self.empty=     False
        self.pair=      pair
        self.interval=  interval
        self.start=     start
        self.end=       end
        
    
    def ToCSV(self, filename, sep=","):
        if self.empty:
            print("No data..")
            return
        self.data.to_csv(filename, sep= sep, index= True)
 
