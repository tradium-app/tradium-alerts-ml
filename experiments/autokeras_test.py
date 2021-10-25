# %% Import libraries
import pandas as pd
import tensorflow as tf
import autokeras as ak
import matplotlib.pyplot as plt
import yfinance

# %% Import data

dataset = yfinance.download("ABNB", "2020-05-16", "2021-10-16")
dataset.reset_index(level=0, inplace=True)
# dataset = pd.read_csv("./data/TSLA.csv")
dataset = dataset.dropna()

# %%
# Prepare data for the Model

predict_from = 1
predict_until = 10
lookback = 10
clf = ak.TimeseriesForecaster(
    lookback=lookback,
    predict_from=predict_from,
    predict_until=predict_until,
    max_trials=1,
    objective="val_loss",
)

val_split = int(len(dataset) * 0.7)
data_train = dataset[:val_split]
validation_data = dataset[val_split:]

data_x = data_train[["Open", "High", "Low", "Volume"]].astype("float64")
data_y = data_train["Close"].astype("float64")

data_x_val = validation_data[["Open", "High", "Low", "Volume"]].astype("float64")
data_y_val = validation_data["Close"].astype("float64")

data_x_test = dataset[["Open", "High", "Low", "Volume"]].astype("float64")

print(data_x.shape)  # (70489, 5)
print(data_y.shape)  # (70489,)

# %% Build the model

# Train the TimeSeriesForecaster with train data
clf.fit(
    x=data_x,
    y=data_y,
    validation_data=(data_x_val, data_y_val),
    batch_size=10,
    epochs=1,
)
# Predict with the best model(includes original training data).
predictions = clf.predict(data_x_test)

plt.plot(predictions)
plt.plot(data_y)

# print(predictions.shape)
# Evaluate the best model with testing data.
# print(clf.evaluate(data_x_val, data_y_val))

