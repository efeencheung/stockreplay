import pandas as pd
import sqlite3

from datetime import date, datetime

class PriceModel():
    def __init__(self):
        self.yestoday_closing_price = 5.39
        (self.year, self.month, self.day) = (2020, 3, 25)
        self.conn = sqlite3.connect('stock.db')        
        self.load()

    def load(self):
        origin_df = pd.read_sql_query("\
            SELECT datetime(time, 'unixepoch', 'localtime') time_index,\
            price, volume FROM sz_300315", self.conn, index_col='time_index')
        origin_df.index = pd.to_datetime(origin_df.index)
        date_str = date(self.year, self.month, self.day).isoformat()
        price = origin_df["price"].resample('60S', label='right', closed='right').last().fillna(method='pad')
        volume = origin_df["volume"].resample('60S', label='right', closed='right').sum()
        df = pd.concat([price, volume], axis=1)
        max_price = df["price"].max()
        min_price = df["price"].min()
        if abs(max_price - self.yestoday_closing_price) > abs(min_price - self.yestoday_closing_price):
            self.max_y = self.yestoday_closing_price + abs(max_price - self.yestoday_closing_price)
            self.min_y = self.yestoday_closing_price - abs(max_price - self.yestoday_closing_price)
        else:
            self.max_y = self.yestoday_closing_price + abs(min_price - self.yestoday_closing_price)
            self.min_y = self.yestoday_closing_price - abs(min_price - self.yestoday_closing_price)
        self.diff_x = 14400
        self.diff_y = self.max_y - self.min_y
        self.min_x = datetime(self.year, self.month, self.day, 9, 30, 00).timestamp()
        self.max_x = self.min_x + 14400
        self.data = []
        for index, row in df.iterrows():
            if index < datetime(self.year, self.month, self.day, 9, 30, 0) or \
                    index > datetime(self.year, self.month, self.day, 15, 0, 0) or \
                    (index > datetime(self.year, self.month, self.day, 11, 30, 0) and \
                    index < datetime(self.year, self.month, self.day, 13, 0, 0)):
                continue

            timestamp = index.timestamp() - 28800
            if index >= datetime(self.year, self.month, self.day, 13, 0, 0):
                timestamp = index.timestamp() - 5400 - 28800

            self.data.append((row["price"], timestamp))

