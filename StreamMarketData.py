#!/usr/bin/env python

import googlefinance as gf
import yahoo_finance as yf
import ystockquote as ysq
import json
from pprint import pprint

class MarketData:
    def __init__(self,symbol):
        self.symbol = symbol

    def streamCurrency(self):
        currency_handler = yf.Currency(self.symbol)
        while True:
            print currency_handler.get_bid()
            stock_handler.refresh() 
   
    def streamStock(self):
        stock_handler = yf.Share(self.symbol)
        #while True:
            #print stock_handler

    def historicalPrice(self,start_date=None,end_date=None):
        stock_handler = yf.Share(self.symbol)
        if start_date == None and end_date == None:
            start_date = stock_handler.get_info()["start"]
            end_date = stock_handler.get_info()["end"]
        historical_data = stock_handler.get_historical(start_date,end_date)

def main():
    marketdata = MarketData("GOOG")
    #marketdata.historicalPrice("2015-05-10","2016-05-13")
    marketdata.historicalPrice()

if __name__ == '__main__':
    main()
