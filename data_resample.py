import sqlite3
import pandas as pd
from datetime import datetime, timezone


if __name__ == "__main__":
    conn = sqlite3.connect('stock.db')
    origin_df = pd.read_sql_query("\
        SELECT datetime(time, 'unixepoch', 'localtime') time_index,\
        code, price, volume FROM tick_l1", conn, index_col='time_index')
    origin_df.index = pd.to_datetime(origin_df.index)
    origin_df["vol"] = origin_df.apply(lambda x: x["price"] * x["volume"], axis=1) 
    origin_df["vol_cumsum"] = origin_df["vol"].cumsum()
    origin_df["volume_cumsum"] = origin_df["volume"].cumsum()
    origin_df["average"] = origin_df.apply(lambda x: round(x["vol_cumsum"] / x["volume_cumsum"], 2), axis=1)

    code = origin_df["code"].resample('60S', label='right', closed='right').last().fillna(method='pad')
    price = origin_df["price"].resample('60S', label='right', closed='right').last().fillna(method='pad')
    volume = origin_df["volume"].resample('60S', label='right', closed='right').sum()
    open = origin_df["price"].resample('60S', label='right', closed='right').first().fillna(method='pad')
    close = origin_df["price"].resample('60S', label='right', closed='right').last().fillna(method='pad')
    high = origin_df["price"].resample('60S', label='right', closed='right').max().fillna(method='pad')
    low = origin_df["price"].resample('60S', label='right', closed='right').min().fillna(method='pad')
    average = origin_df["average"].resample('60S', label='right', closed='right').last().fillna(method='pad')
    df = pd.concat([code, price, volume, open, close, high, low, average], \
        keys=['code', 'price', 'volume', 'open', 'close', 'high', 'low', 'average'], \
        axis=1)
    df = df[((df.index>=datetime(2020,3,25,9,30,0)) & (df.index<=datetime(2020,3,25,11,30,0))) \
        | ((df.index>=datetime(2020,3,25,13,0,0)) & (df.index<=datetime(2020,3,25,15,0,0)))]
    time = df.index.to_series(name='time')
    time = time.apply(lambda x: int(x.timestamp() - 28800))
    df['time'] = time
    print(df)
    #df.to_sql('data_1m', conn, if_exists='append', index=False)
