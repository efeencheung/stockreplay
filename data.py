import sqlite3
import pandas as pd
from datetime import datetime


if __name__ == "__main__":
    date = '2020-03-25'

    df = pd.read_csv('300315.csv')
    df = df.drop(columns = ['TranID'])
    df = df.rename(columns={"Time": "time", "Price": "price", \
        "Volume": "volume", "SaleOrderVolume": "sale_order_volume", \
        "BuyOrderVolume": "buy_order_volume", "Type": "type", \
        "SaleOrderID": "sale_order_id", "SaleOrderPrice": "sale_order_price", \
        "BuyOrderID": "buy_order_id", "BuyOrderPrice": "buy_order_price"})

    codes = pd.Series(['300315'])
    codes = codes.repeat(len(df['time']))
    codes.index = df['time'].index
    df['code'] = codes
    df['time'] = df['time'].apply(lambda x: int(datetime.fromisoformat(date+' '+x).timestamp()))

    conn = sqlite3.connect('stock.db')
    df.to_sql('tick_l1', conn, if_exists='append', index=False)
