###################################################
#####                Import                   #####
###################################################

# data visualization
from ast import If
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd

# yahoo finance api library (private use only!)
import yfinance as yf
yf.pdr_override()

# date picker
from datetime import datetime, timedelta

# config
import json
with open('stock_info.json', 'r') as config_file:
    config = json.load(config_file)

###################################################
#####                  Data                   #####
###################################################

# data from yesterday until today
start_date = datetime.strftime((datetime.now() - timedelta(1)), '%Y-%m-%d')
end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

print("Download: ")
# get eur-usd price
eur_usd = pdr.get_data_yahoo("EURUSD=X", period = "1d", interval = "1d", auto_adjust = True, group_by = 'ticker').iat[0,3]

tickerStrings = ['AAPL', 'AMZN']

# use sets to avoid duplicates of symbols
stocks = set()
cryptos = set()
etfs = set()

# get stock/etf/crypto symbols if desired
if config['info']['stocks']:
    for stock in config['stocks']:
        stocks.add(stock['symbol'])

if config['info']['etfs']:
    for etf in config['etfs']:
        etfs.add(etf['symbol'])

if config['info']['cryptos']:
    for crypto in config['cryptos']:
        cryptos.add(crypto['symbol'])

# data frame list for all stocks, etfs and cryptos
df_list = list()

# get stocks if desired
if config['info']['stocks']:
    for ticker in stocks:
        # get yahoo finance data
        data = yf.download(ticker, group_by="Ticker", start=start_date, end=end_date, interval = "1h", auto_adjust = True)
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

# get stocks if desired
if config['info']['etfs']:
    for ticker in etfs:
        # get yahoo finance data
        data = yf.download(ticker, group_by="Ticker", start=start_date, end=end_date, interval = "1h", auto_adjust = True)
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

# get stocks if desired
if config['info']['cryptos']:
    for ticker in cryptos:
        # get yahoo finance data
        data = yf.download(ticker, group_by="Ticker", start=start_date, end=end_date, interval = "1h", auto_adjust = True)
        data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
        df_list.append(data)

# combine all dataframes into a single dataframe
df = pd.concat(df_list)

###################################################
#####              Visualization              #####
###################################################

# save to csv
df.to_csv('ticker.csv')