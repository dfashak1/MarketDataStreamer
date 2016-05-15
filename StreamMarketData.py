#!/usr/bin/env python
import argparse
import googlefinance as gf
import yahoo_finance as yf
import ystockquote as ysq
import json
from pprint import pprint
import datetime as dt
import csv

class JSONHandler:
    def __init__(self,json):
        self.json_list = json

    def convertToCSV(self,filename):
        with open(filename,"w") as csvfile:
            fieldnames = self.json_list[0].keys()
            writer = csv.DictWriter(csvfile,fieldnames)
            writer.writeheader()
            for json in self.json_list:
                writer.writerow(json)
            
class MarketData:
    def __init__(self,symbol):
        self.symbol = symbol
        self.end = False

    def streamCurrency(self):
        currency_handler = yf.Currency(self.symbol)
        while True:
            try:
                print currency_handler.get_bid()
                currency_handler.refresh() 
            except KeyboardInterrupt:
                self.end = True 
   
    def streamStock(self):
        stock_handler = yf.Share(self.symbol)
        while True:
            try:
                print stock_handler
            except KeyboardInterrupt:
                self.end = True

    def historicalPrice(self,start_date=None,end_date=None,duration=None):
        stock_handler = yf.Share(self.symbol)
        if start_date == None and end_date == None and duration == None:
            start_date = stock_handler.get_info()["start"]
            end_date = stock_handler.get_info()["end"]
        elif duration is not None:
            if "day" in duration.lower():
                end_date = stock_handler.get_info()["end"]
                end_date_as_dt = dt.datetime.strptime(end_date,"%Y-%m-%d")
                start_date = end_date_as_dt - dt.timedelta(days=int(duration.split()[0]))
                start_date = start_date.strftime("%Y-%m-%d")
            elif "week" in duration.lower():
                end_date = stock_handler.get_info()["end"]
                end_date_as_dt = dt.datetime.strptime(end_date,"%Y-%m-%d")
                start_date = end_date_as_dt - dt.timedelta(weeks=int(duration.split()[0]))
                start_date = start_date.strftime("%Y-%m-%d")
            elif "month" in duration.lower():
                end_date = stock_handler.get_info()["end"]
                end_date_as_dt = dt.datetime.strptime(end_date,"%Y-%m-%d")
                start_date = end_date_as_dt - dt.timedelta(months=int(duration.split()[0]))
                start_date = start_date.strftime("%Y-%m-%d")
            elif "year" in duration.lower():
                end_date = stock_handler.get_info()["end"]
                end_date_as_dt = dt.datetime.strptime(end_date,"%Y-%m-%d")
                start_date = end_date_as_dt - dt.timedelta(years=int(duration.split()[0]))
                start_date = start_date.strftime("%Y-%m-%d")
            else:
                print "Please enter a valid duration in days, weeks, months or years"
        historical_data = stock_handler.get_historical(start_date,end_date)
        return(historical_data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action = "store", dest = "symbol", help = "Symbol that you want to analyze e.g. 'BABA', 'GOOG', 'FB'")
    parser.add_argument("-sl", action = "store", dest = "symbol_list", help = "Symbol list that you want to analyze e.g. 'BABA, GOOG, FB'")
    parser.add_argument("-si", action = "store", dest = "stock_index", help = "Stock index that you want to analyze e.g. 'NASDAQ', 'SP500' and 'DJIA'")
    parser.add_argument("-sd", action = "store", dest = "start_date", help = "Start date of historical analysis for stock in format 'yyyy-mm-dd'")
    parser.add_argument("-st", action = "store_true", dest = "stream", help = "Stream market data from symbol or just symbolist")
    parser.add_argument("-ed", action = "store", dest = "end_date", help = "End date of historical analysis for stock in format 'yyyy-mm-dd'")
    parser.add_argument("-td", action = "store", dest = "time_duration", help = "Time duration from end date on when to analyze stock could be in days, weeks, months or years e.g. 2 weeks")
    args = parser.parse_args()
    
    if args.symbol:
        marketdata = MarketData(args.symbol)
        if args.start_date and args.end_date:
            historical_data_json = marketdata.historicalPrice(args.start_date,args.end_date,None)   
            jsonhandler = JSONHandler(historical_data_json)
            jsonhandler.convertToCSV(args.symbol+".csv")
        elif args.time_duration:
            historical_data_json = marketdata.historicalPrice(None,None,args.time_duration)
            jsonhandler = JSONHandler(historical_data_json)
            jsonhandler.convertToCSV(args.symbol+".csv")
        elif args.stream:
            marketdata.streamCurrency()
        else:
            print "Please pass in the right parameters....run the program with -h to know what you need to do"
    else:
        print "Please pass in a symbol to analyze" 

if __name__ == '__main__':
    main()
