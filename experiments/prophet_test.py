# %% Import libraries
from datetime import datetime
import sys

sys.path.insert(0, "../")
import numpy as np
import pandas as pd
import fbprophet
import matplotlib.pyplot as plt
import yfinance

# %% Read data
df = yfinance.download("BABA", "2020-05-16", "2021-11-07")
X = np.array(df["Close"])

stock_history = df[["Close"]]
stock_history.reset_index(level=0, inplace=True)
stock_history.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

# %% create model
model = fbprophet.Prophet(
    daily_seasonality=False,
    weekly_seasonality=False,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05,
    changepoints=None,
)

model.fit(stock_history)

# %% Make Predictions

future = model.make_future_dataframe(periods=30, freq="D")
future = model.predict(future)

plt.plot(stock_history["ds"], stock_history["y"])
plt.plot(future["ds"], future["yhat"])

prediction = future[["ds", "yhat"]].tail(40)
prediction.rename(columns={"ds": "time", "yhat": "close"}, inplace=True)

prediction[["time"]] = prediction["time"].apply(lambda x: int(x.timestamp() * 1000))

# plt.plot(
#     prediction["time"].apply(lambda x: datetime.utcfromtimestamp(x / 1000)),
#     prediction["close"],
# )


prediction.to_dict("records")
