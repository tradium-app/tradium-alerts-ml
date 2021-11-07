# %%
import sys

sys.path.insert(0, "../")
import fbprophet
from datetime import datetime
import logging
from db_manager import DBManager
from utilities.mongo_connection import get_db_connection

logging.root.setLevel(logging.INFO)


class ProphetPredictor:
    def predict(self):
        stockClosePriceMaps = DBManager().loadStockHistory()

        stockPredictions = self.buildModelAndRunPredictions(stockClosePriceMaps)
        self.saveModel(stockPredictions)

        logging.info(f"ProphetPredictor rat at {datetime.now()}.")
        return stockPredictions

    def buildModelAndRunPredictions(self, stockClosePriceMaps):
        stockPredictions = {}
        for symbol in stockClosePriceMaps:
            logging.info(f"Build Prophet model for {symbol}.")

            model = fbprophet.Prophet(
                daily_seasonality=False,
                weekly_seasonality=False,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05,
                changepoints=None,
            )

            df = stockClosePriceMaps[symbol].filter(['date', 'close'])
            df.rename(columns={"date": "ds", "close": "y"}, inplace=True)
            model.fit(df)

            future = model.make_future_dataframe(periods=30, freq="D")
            future = model.predict(future)
            stockPredictions[symbol] = future[["ds", "yhat"]].tail(40)

        return stockPredictions

    def saveModel(self, stockPredictions):
        conn = get_db_connection()
        stockHistoryCol = conn["salertdb"]["stockHistory"]

        for symbol in stockPredictions:
            df = stockPredictions[symbol]
            df.rename(columns={"ds": "time", "yhat": "close"}, inplace=True)

            df["time"] = df["time"].apply(lambda x: int(x.timestamp() * 1000))

            stockHistoryCol.update_one(
                {"symbol": symbol},
                {"$set": {"model_predictions": df.to_dict("records")}},
            )


if __name__ == "__main__":
    predictor = ProphetPredictor()
    stockPredictions = predictor.predict()
