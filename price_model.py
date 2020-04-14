import pandas as pd
import sqlite3

from datetime import datetime

class PriceModel():
    def __init__(self):
        self.yestoday_closing_price = 5.39
        (self.year, self.month, self.day) = (2020, 3, 25)
        self.conn = sqlite3.connect('stock.db')        

    def load(self):
        origin_df = pd.read_sql_query("\
            SELECT datetime(time, 'unixepoch', 'localtime') time_index,\
            price, volume FROM sz_300315", self.conn, index_col='time_index')
        origin_df.index = pd.to_datetime(origin_df.index)
        start1 = str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " 09:30:00"
        end1 = str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " 11:30:00"
        start2 = str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " 13:00:00"
        end2 = str(self.year) + "-" + str(self.month) + "-" + str(self.day) + " 15:00:00"
        query_str = "(index >= start1 and index <= end1) or"
        origin_df.query(" \
                (index >= start2 and index <= end2)", inplace = True)
        
        print(origin_df)

        """
        price = self.origin_df["price"].resample('60S', label='right', closed='right').last()
        volume = self.origin_df["volume"].resample('60S', label='right', closed='right').sum()
        self.df = pd.concat([price, volume], axis=1)
        max_price = self.df["price"].max()
        min_price = self.df["price"].min()
        prev_price = 5.39
        if abs(max_price - prev_price) > abs(min_price - prev_price):
            self.max_y = prev_price + abs(max_price - prev_price)
            self.min_y = prev_price - abs(max_price - prev_price)
        else:
            self.max_y = prev_price + abs(min_price - prev_price)
            self.min_y = prev_price - abs(min_price - prev_price)
        self.diff_x = 14400
        self.diff_y = self.max_y - self.min_y
        self.min_x = datetime(2020, 3, 25, 9, 30, 00).timestamp()
        """

if __name__ == "__main__":
    price = PriceModel()
    price.load()
