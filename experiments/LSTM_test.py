# %%
# Make sure that you have all these libaries available to run the code successfully
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf  # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

# %%
# Import data


df = pd.read_csv("./data/TSLA.csv")
df = df.filter(["closePrice"])
df = df.tail(10000)

df.plot()

# %%
# Prepare data
len_train = int(len(df) * 0.7)

train_data = df.iloc[:len_train]
test_data = df.iloc[len_train:]

# Normalize data
scaler = MinMaxScaler()
# train_data = train_data.reshape(-1,1)
# test_data = test_data.reshape()

window = 2500

# train_data.iloc[0:0+smoothing_window_size,:]
# di = 0
# scaler.fit(train_data.iloc[di : di + window, :])
# train_data.iloc[di : di + window, :] = scaler.transform(
#     train_data.iloc[di : di + window, :]
# )

for di in range(0, len(train_data), window):
    scaler.fit(train_data.iloc[di : di + window, :])
    train_data.iloc[di : di + window, :] = scaler.transform(
        train_data.iloc[di : di + window, :]
    )

for di in range(0, len(test_data), window):
    scaler.fit(test_data.iloc[di : di + window, :])
    test_data.iloc[di : di + window, :] = scaler.transform(
        test_data.iloc[di : di + window, :]
    )

# %%
# Smoothe train data using EMA to remove raggedness

EMA = 0.0
gamma = 0.1
for ti in range(len(train_data)):
    EMA = gamma * train_data.iloc[ti] + (1 - gamma) * EMA
    train_data.iloc[ti] = EMA

all_mid_data = np.concatenate([train_data, test_data], axis=0)

# %%
# window_size = 100
# N = train_data.size
# std_avg_predictions = []
# std_avg_x = []
# mse_errors = []

# for pred_idx in range(window_size, N):

#     if pred_idx >= N:
#         date = dt.datetime.strptime(k, "%Y-%m-%d").date() + dt.timedelta(days=1)
#     else:
#         date = df.loc[pred_idx, "Date"]

#     std_avg_predictions.append(np.mean(train_data[pred_idx - window_size : pred_idx]))
#     mse_errors.append((std_avg_predictions[-1] - train_data[pred_idx]) ** 2)
#     std_avg_x.append(date)

# print("MSE error for standard averaging: %.5f" % (0.5 * np.mean(mse_errors)))

# %%
