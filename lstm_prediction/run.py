# %%

import os
import sys

# sys.path.insert(0, "core")
sys.path.append("core")
import json
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
import yfinance
from core.data_processor import DataLoader
from core.model import Model


def main():
    configs = json.load(open("config.json", "r"))

    # downloadStockHistory(["QQQ"])

    data = DataLoader(
        os.path.join("../data", "TSLA.csv"),
        configs["data"]["train_test_split"],
        configs["data"]["columns"],
    )

    model = Model()
    model.build_model(configs)
    x, y = data.get_train_data(
        seq_len=configs["data"]["sequence_length"],
        normalise=configs["data"]["normalise"],
    )

    """
	# in-memory training
	model.train(
		x,
		y,
		epochs = configs['training']['epochs'],
		batch_size = configs['training']['batch_size'],
		save_dir = configs['model']['save_dir']
	)
	"""
    # out-of memory generative training
    steps_per_epoch = math.ceil(
        (data.len_train - configs["data"]["sequence_length"])
        / configs["training"]["batch_size"]
    )
    model.train_generator(
        data_gen=data.generate_train_batch(
            seq_len=configs["data"]["sequence_length"],
            batch_size=configs["training"]["batch_size"],
            normalise=configs["data"]["normalise"],
        ),
        epochs=configs["training"]["epochs"],
        batch_size=configs["training"]["batch_size"],
        steps_per_epoch=steps_per_epoch,
        save_dir=configs["model"]["save_dir"],
    )

    x_test, y_test = data.get_test_data(
        seq_len=configs["data"]["sequence_length"],
        normalise=configs["data"]["normalise"],
    )

    predictions = model.predict_sequences_multiple(
        x_test, configs["data"]["sequence_length"], configs["data"]["sequence_length"]
    )
    # predictions = model.predict_sequence_full(x_test, configs['data']['sequence_length'])
    # predictions = model.predict_point_by_point(x_test)

    plot_results_multiple(predictions.iloc[1000:,:], y_test, configs["data"]["sequence_length"])
    # plot_results(predictions, y_test)


def downloadStockHistory(symbols):
    today = datetime.today().strftime("%Y-%m-%d")
    oneYearAgo = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

    stockClosePriceMaps = {}
    for symbol in symbols:
        df = yfinance.download(symbol, oneYearAgo, today)

        stock_file_path = "../data/" + symbol + ".csv"
        df.to_csv(path_or_buf=stock_file_path, header=True)

        stock_history = df[["Close"]]
        stock_history.reset_index(level=0, inplace=True)
        stock_history.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)
        stockClosePriceMaps[symbol] = stock_history

    return stockClosePriceMaps


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor="white")
    ax = fig.add_subplot(111, figsize=(15,15))
    ax.plot(true_data, label="True Data")
    plt.plot(predicted_data, label="Prediction")
    plt.legend()
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor="white")
    ax = fig.add_subplot(111, figsize=(15,15))
    ax.plot(true_data, label="True Data")
    # Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label="Prediction")
        plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
