# %%
import sys

sys.path.insert(0, "../")
import yfinance
from datetime import datetime, timedelta
import logging
import pymongo
import pandas as pd
from db_manager import DBManager
from utilities.mongo_connection import get_db_connection
from environs import Env

logging.root.setLevel(logging.INFO)

env = Env()
env.read_env()

# %%
# function definitions
def loadStockHistory(symbols):
    today = datetime.today().strftime("%Y-%m-%d")
    oneYearAgo = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    stockClosePriceMaps = {}
    for symbol in symbols:
        df = yfinance.download(symbol, oneYearAgo, today)
        del df["Close"]
        df.reset_index(level=0, inplace=True)
        df['symbol'] = symbol
        df['time'] = df['Date'].apply(lambda x: (pd.to_datetime(x) - pd.to_datetime('1970-01-01')).total_seconds()*1000)

        df.rename(columns={"Adj Close": "Close"}, inplace=True)
        df.columns= df.columns.str.lower()
        stockClosePriceMaps[symbol] = df

    return stockClosePriceMaps


# %%

# symbols = DBManager().loadStockHistory()

stockClosePriceMaps = loadStockHistory(['BABA'])

# stockClosePriceMaps['BABA']['time'] = (pd.to_datetime(stockClosePriceMaps['BABA']['Date']) - pd.to_datetime('1970-01-01')).total_seconds()*1000


stockClosePriceMaps['BABA']['Date'].apply(lambda x: (pd.to_datetime(x) - pd.to_datetime('1970-01-01')).total_seconds()*1000)


stockClosePriceMaps['BABA']


pd.Timestamp('2020-11-10')

# datetime(1970,1,1).date

mongodb_uri = env("mongodb_uri")
mongoClient = pymongo.MongoClient(mongodb_uri)
salertdb = mongoClient["salertdb"]
stockCol = salertdb["stockHistory"]

stockClosePriceMaps["BABA"]["symbol"] = "BABA"


# %%

symbols = DBManager().loadStockHistory()
stockClosePriceMaps = loadStockHistory(symbols)


for symbol in stockClosePriceMaps:
    stockCol.update_one({"symbol": symbol}, {"$set": {"daily_priceHistory": stockClosePriceMaps[symbol].to_dict("records")}})
