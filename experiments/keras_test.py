# %% Import libraries
import math
import numpy as np
import pandas as pd
import random as rn
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

rn.seed(0)
np.random.seed(0)
tf.random.set_seed(0)

plt.style.use("fivethirtyeight")

#%% Import dataframe
df = pd.read_csv("./data/TSLA.csv")
df = df.filter(["closePrice"])
df = df.tail(10000)

dataset = df.values
features_length = dataset.shape[1]
