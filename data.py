import sqlite3
import pandas as pd


if __name__ == "__main__":
    conn = sqlite3.connect('stock.db')

    df = pd.read_csv('300315.csv')
    df.to_sql('tick_l1', conn)
