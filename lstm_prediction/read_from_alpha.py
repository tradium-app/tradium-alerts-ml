# %%
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from environs import Env

env = Env()
env.read_env('../.env')

ts = TimeSeries(key=env('alphavantage_api_key'), output_format='pandas', indexing_type='date')
data, meta_data = ts.get_intraday_extended(symbol='NFLX',interval='60min')

data = data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})

plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()

data['4. close'].plot()

data.to_csv('../data/NFLX.CSV')
