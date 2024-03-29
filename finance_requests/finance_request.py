"""Finance API Requester

This class allows the user to request desired stock informations.

For this purpose the class use the "free" finance api from alpha vantage.
It allows 500 request a day and 5 request per minute.

"""
import datetime
import json
import time

import matplotlib.pyplot as plt
# plotting
import pandas as pd
import requests


class requester:
    base_url = "https://www.alphavantage.co/query?"
    usdEuroExchangeRate = 1

    """ Constructor """
    def __init__(self, api_key: str = "", config_path: str = ""):
        with open(config_path, 'r') as config_file:
                self.config = json.load(config_file)

        # use sets to avoid duplicates of symbols
        self.stocks = set()
        self.cryptos = set()
        self.etfs = set()
          
        # get stock/etf/crypto symbols if desired
        if self.config['info']['stocks']:
            for stock in self.config['stocks']:
                self.stocks.add(stock['symbol'])

        if self.config['info']['etfs']:
            for etf in self.config['etfs']:
                self.etfs.add(etf['symbol'])

        if self.config['info']['cryptos']:
            for crypto in self.config['cryptos']:
                self.cryptos.add(crypto['symbol'])

        if api_key != "" and config_path != "":
            self.api_key = api_key
            
            self.usdEuroExchangeRate = self.getExchangeRate('USD', 'EUR')
            time.sleep(12)


    """ Get stock, etf and crypto data
    (the last 7 days (stock and etf without the weekend)) """
    def getDataDaily(self):
        data = dict()

        data["stocks"] = self.getStocksDaily()
        data["etfs"] = self.getEtfsDaily()
        data["cryptos"] = self.getCryptosDaily()

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    def getExchangeRate(self, fromSymbol, toSymbol):
        function_name = "function=FX_DAILY"

        # get data
        url = self.base_url + function_name + '&from_symbol=' + fromSymbol + '&to_symbol=' + toSymbol + '&apikey=' + self.api_key
        r = requests.get(url)
        data = dict(r.json()["Time Series FX (Daily)"])

        # request only 5 times in a minute
        time.sleep(12)

        # return only 'close' of today
        return float(data[datetime.datetime.today().strftime('%Y-%m-%d')]["4. close"])

    def getStocksDaily(self):
        stocks_list = dict()

        # get data for each symbol
        for symbol in self.stocks:
            stocks_list[symbol] = self.getStockOrEtfDaily(symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return stocks_list

    def getEtfsDaily(self):
        etfs_list = dict()

        # get data for each symbol
        for symbol in self.etfs:
            etfs_list[symbol] = self.getStockOrEtfDaily(symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return etfs_list

    def getCryptosDaily(self):
        cryptos_list = dict()

        # get data for each symbol
        for symbol in self.cryptos:
            cryptos_list[symbol] = self.getCryptoDaily(symbol)
            # request only 5 times in a minute
            time.sleep(12)
        
        return cryptos_list

    def getStockOrEtfDaily(self, symbol):
        function_name = "function=TIME_SERIES_DAILY_ADJUSTED"
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
                # currency conversion
                price = float(stock_info["4. close"]) * self.usdEuroExchangeRate
                data_reduced[date.strftime('%d.%m')] = price

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
                # currency conversion
                price = float(crypto_info["4a. close (USD)"]) * self.usdEuroExchangeRate
                data_reduced[date.strftime('%d.%m')] = price

        return data_reduced

    def getRequestedData(self):
        with open('./data.json') as handle:
            dictdump = json.loads(handle.read())
        return dictdump

    def plotCourse(self, userid : str):
        data = self.getRequestedData()
        
        # plot stocks
        df = pd.DataFrame(data["stocks"])
        df.plot()
        #plt.show()
        plt.savefig('./plots/stocks_' + userid + '.png')
        #print(df.to_markdown())

        # plot etfs
        df = pd.DataFrame(data["etfs"])
        df.plot()
        #plt.show()
        plt.savefig('./plots/etfs_' + userid + '.png')

        # plot crytos
        df = pd.DataFrame(data["cryptos"])
        df.plot()
        #plt.show()
        plt.savefig('./plots/cryptos_' + userid + '.png')

    def plotStockBalance(self, userid: str):
        data = self.getRequestedData()
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        today = today.strftime('%d.%m')

        balance_calc = dict()
        count = 0

        # get total price of stocks 
        for symbol in self.stocks:
            # save all dates with price
            current_prices = data["stocks"][symbol]
            stock_quantity = self.config["stocks"][count]["quantity"]

            stock_balance = dict()

            for stock_date, stock_price in current_prices.items():
                if stock_date in balance_calc:
                    stock_balance[stock_date] = stock_balance[stock_date] + stock_price * stock_quantity
                else:
                    stock_balance[stock_date] = stock_price * stock_quantity
            
            balance_calc[symbol] = stock_balance
            count += 1

        # plot stocks
        df = pd.DataFrame(balance_calc)
        df.plot()
        plt.savefig('./plots/stocks_balance_detailed_' + userid + '.png')

        stock_balance = dict()
        count = 0
        buy_in = 0

        balance_mean = 0

        # get total price of stocks 
        for symbol in self.stocks:
            # save all dates with price
            current_prices = data["stocks"][symbol]
            stock_quantity = self.config["stocks"][count]["quantity"]

            buy_in += self.config["stocks"][count]["total_price"]

            for stock_date, stock_price in current_prices.items():
                if stock_date in stock_balance:
                    balance_mean += stock_price * stock_quantity
                    stock_balance[stock_date] = stock_balance[stock_date] + stock_price * stock_quantity
                else:
                    balance_mean += stock_price * stock_quantity
                    stock_balance[stock_date] = stock_price * stock_quantity
            count += 1

        balance_mean = balance_mean / len(stock_balance.keys())

        plot_balance = dict()
        plot_balance["ALL"] = stock_balance

        # plot stocks
        df = pd.DataFrame(plot_balance)

        # plot buy-in line
        if (balance_mean - buy_in)  > 500:
            df.plot(color="green")
        elif (balance_mean - buy_in) < -500:
            df.plot(color="red")
        else: 
            plt.axhline(y=buy_in, color='r', linestyle='-')
        
        plt.savefig('./plots/stocks_balance_' + userid + '.png')