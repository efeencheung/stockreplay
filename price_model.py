import pandas as pd
import sqlite3

from datetime import datetime


class PriceModel():
    def __init__(self):
        self.yestoday_close = 5.39
        (self.year, self.month, self.day) = (2020, 3, 25)

        conn = sqlite3.connect('stock.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(price) high, MIN(price) low FROM tick_l1')
        (high, low) = cursor.fetchone()

        if abs(high - self.yestoday_close) > abs(low - self.yestoday_close):
            self.max_y = round(self.yestoday_close +
                               abs(high - self.yestoday_close), 2)
            self.min_y = round(self.yestoday_close -
                               abs(high - self.yestoday_close), 2)
        else:
            self.max_y = round(self.yestoday_close +
                               abs(low - self.yestoday_close), 2)
            self.min_y = round(self.yestoday_close - abs(low -
                               self.yestoday_close), 2)
        self.diff_x = 14400
        self.diff_y = self.max_y - self.min_y
        self.min_x = datetime(self.year, self.month, self.day,
                              9, 30, 00).timestamp()
        self.max_x = self.min_x + 14400

        self.df = pd.read_sql_query("SELECT time, price, volume, average,\
                                    direction FROM data_1m", conn)
        self.max_vol = self.df["volume"].max()
        self.data = []
        self.vol_data = []
        for index, row in self.df.iterrows():
            if row["time"] >= datetime(self.year, self.month,
                                       self.day, 13, 0, 0).timestamp():
                row["time"] = row["time"] - 5400

            self.data.append((row["time"], row["price"]))

            if row["open"] > row["close"]:
                type = "short"
            elif row["open"] < row["close"]:
                type = "long"
            else:
                type = "flat"
            self.vol_data.append((row["time"], row["volume"], type))
