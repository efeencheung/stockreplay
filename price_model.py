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
        self.origin_df = pd.read_sql_query("\
            SELECT datetime(time, 'unixepoch', 'localtime') time_index,\
            price, volume FROM tick_l1", self.conn, index_col='time_index')
        self.origin_df.index = pd.to_datetime(self.origin_df.index)

        max_price = self.origin_df["price"].max()
        min_price = self.origin_df["price"].min()
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
    
        self.time_data = self.data_deal('60S')
        self.tick_data = self.data_deal('1S')

    def data_deal(self, time_interval):
        price = self.origin_df["price"].resample(time_interval, label='right', closed='right').last().fillna(method='pad')
        volume = self.origin_df["volume"].resample(time_interval, label='right', closed='right').sum()
        opening_price = self.origin_df["price"].resample(time_interval, label='right', closed='right').first()
        closing_price = self.origin_df["price"].resample(time_interval, label='right', closed='right').last()
        max_price = self.origin_df["price"].resample(time_interval, label='right', closed='right').max()
        min_price = self.origin_df["price"].resample(time_interval, label='right', closed='right').min()
        df = pd.concat([price, volume, opening_price, closing_price, max_price, min_price], \
            keys=['price', 'volume', 'opening_price', 'closing_price', 'max_price', 'min_price'], \
            axis=1)
        data = []
        for index, row in df.iterrows():
            if index < datetime(self.year, self.month, self.day, 9, 30, 0) or \
                    index > datetime(self.year, self.month, self.day, 15, 0, 0) or \
                    (index > datetime(self.year, self.month, self.day, 11, 30, 0) and \
                    index < datetime(self.year, self.month, self.day, 13, 0, 0)):
                continue

            timestamp = index.timestamp() - 28800
            if index >= datetime(self.year, self.month, self.day, 13, 0, 0):
                timestamp = index.timestamp() - 5400 - 28800

            data.append((timestamp, row["price"], row["volume"], row["opening_price"], \
                    row["closing_price"], row["max_price"], row["min_price"]))

        return data
    
