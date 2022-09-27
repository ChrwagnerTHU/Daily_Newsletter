"""Finance API Requester

This class allows the user to request desired stock informations.

For this purpose the class use the "free" finance api from alpha vantage.
It allows 500 request a day and 5 request per minute.

"""
import requests
import datetime
import json
import time

class requester:
    base_url = "https://www.alphavantage.co/query?"

    """ Constructor """
    def __init__(self, api_key, config_path: str):
        self.api_key = api_key

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        # use sets to avoid duplicates of symbols
        self.stocks = set()
        self.cryptos = set()
        self.etfs = set()
        
        # get stock/etf/crypto symbols if desired
        if config['info']['stocks']:
            for stock in config['stocks']:
                self.stocks.add(stock['symbol'])

        if config['info']['etfs']:
            for etf in config['etfs']:
                self.etfs.add(etf['symbol'])

        if config['info']['cryptos']:
            for crypto in config['cryptos']:
                self.cryptos.add(crypto['symbol'])

    """ Get stock, etf and crypto data
    (the last 7 days (stock and etf without the weekend)) """
    def getDataDaily(self):
        data = list()

        data += self.getStocksDaily()
        data += self.getEtfsDaily()
        data += self.getCryptosDaily()

        return data

    def getStocksDaily(self):
        stocks_list = list()

        # get data for each symbol
        for symbol in self.stocks:
            stock_with_symbol = dict()
            stock_with_symbol[symbol] = self.getStockOrEtfDaily(symbol)
            stocks_list.append(stock_with_symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return stocks_list

    def getEtfsDaily(self):
        etfs_list = list()

        # get data for each symbol
        for symbol in self.etfs:
            etf_with_symbol = dict()
            etf_with_symbol[symbol] = self.getStockOrEtfDaily(symbol)
            etfs_list.append(etf_with_symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return etfs_list

    def getCryptosDaily(self):
        cryptos_list = list()

        # get data for each symbol
        for symbol in self.cryptos:
            crypto_with_symbol = dict()
            crypto_with_symbol[symbol] = self.getCryptoDaily(symbol)
            cryptos_list.append(crypto_with_symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return cryptos_list

    def getStockOrEtfDaily(self, symbol):
        function_name = "function=TIME_SERIES_DAILY"
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        # get data
        url = self.base_url + function_name + '&symbol=' + symbol + '&apikey=' + self.api_key
        r = requests.get(url)
        data = dict(r.json()["Time Series (Daily)"])
        
        # remove unnessesary data
        data_reduced = dict()
        for stock_date, stock_info in data.items():
            date = datetime.datetime.strptime(stock_date, '%Y-%m-%d')
            delta = today - date

            if delta.days < 7:
                data_reduced[stock_date] = stock_info

        return data_reduced

    def getCryptoDaily(self, symbol):
        function_name = "function=DIGITAL_CURRENCY_DAILY"
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        # get data
        url = self.base_url + function_name + '&symbol=' + symbol + '&market=USD' + '&apikey=' + self.api_key
        r = requests.get(url)
        data = dict(r.json()["Time Series (Digital Currency Daily)"])
        
        # remove unnessesary data
        data_reduced = dict()
        for crypto_date, crypto_info in data.items():
            date = datetime.datetime.strptime(crypto_date, '%Y-%m-%d')
            delta = today - date

            if delta.days < 7:
                data_reduced[crypto_date] = crypto_info

        return data_reduced