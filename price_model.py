import pandas as pd
import sqlite3

from datetime import date, datetime

class PriceModel():
    def __init__(self):
        self.yestoday_closing_price = 5.39
        (self.year, self.month, self.day) = (2020, 3, 25)
        self.conn = sqlite3.connect('stock.db')        
        self.df = pd.read_sql_query("\
            SELECT time, price FROM data_1m", self.conn)

        max_price = self.df["price"].max()
        min_price = self.df["price"].min()
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

        self.data = self.data_deal()

    def data_deal(self):
        data = []
        for index, row in self.df.iterrows():
            if row["time"] >= datetime(self.year, self.month, self.day, 13, 0, 0).timestamp():
                row["time"] = row["time"] - 5400

            data.append((row["time"], row["price"]))

        return data
    
