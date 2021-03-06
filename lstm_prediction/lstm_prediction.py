# %%
import os
import sys
import pandas as pd
sys.path.insert(0, "../")
import json
import math
from datetime import datetime
import logging
from db_manager import DBManager
from utilities.mongo_connection import get_db_connection
from lstm_prediction.core.data_processor import DataLoader
from lstm_prediction.core.model import Model

logging.root.setLevel(logging.INFO)

class LstmPredictor:
    def predict(self):
        stockClosePriceMaps = DBManager().loadStockHistory()
        stockPredictions = self.buildModelAndRunPredictions(stockClosePriceMaps)

        self.saveModel(stockPredictions)

        logging.info(f"LstmPredictor rat at {datetime.now()}.")
        return stockPredictions

    def buildModelAndRunPredictions(self, stockClosePriceMaps):
        stockPredictions = {}

        config_file_path = os.path.join(os.path.dirname(__file__), './config.json')
        configs = json.load(open(config_file_path, "r"))
        if not os.path.exists(configs["model"]["save_dir"]):
            os.makedirs(configs["model"]["save_dir"])

        for symbol in stockClosePriceMaps:
            logging.info(f"Build LSTM model for {symbol}.")

            try:
                data_file_path = os.path.join(os.path.dirname(__file__), "../data/watchlist_df.csv")
                print(data_file_path)
                data = DataLoader(
                    data_file_path,
                    symbol,
                    configs["data"]["train_test_split"],
                    configs["data"]["columns"],
                )

                model = Model()
                model.build_model(configs)
                # x, y = data.get_train_data(
                #     seq_len=configs["data"]["sequence_length"],
                #     normalise=configs["data"]["normalise"],
                # )

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

                prediction_input = stockClosePriceMaps[symbol].filter(['volume', 'close']).tail(49).to_numpy()

                predictions = model.predict_sequence_future(prediction_input, configs["data"]["sequence_length"], 40)

                stockPredictions[symbol] = predictions
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                pass

        return stockPredictions

    def saveModel(self, stockPredictions):
        conn = get_db_connection()
        stockHistoryCol = conn["salertdb"]["stockHistory"]

        for symbol in stockPredictions:
            df = stockPredictions[symbol]
            df = pd.DataFrame(df, columns =['close'])

            stockHistoryCol.update_one(
                {"symbol": symbol},
                {"$set": {"model_predictions_2": df.to_dict("records")}},
            )


if __name__ == "__main__":
    predictor = LstmPredictor()
    stockPredictions = predictor.predict()
