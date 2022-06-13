import time

import pyupbit
import numpy as np


def get_ror(k=0.5):
    #df = pyupbit.get_ohlcv("KRW-XRP",interval="minute720" ,count=200)
    df = pyupbit.get_ohlcv("KRW-XRP", interval="day", count=100)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    time.sleep(0.1)
    fee = 0.001
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.05):

    ror = get_ror(k)
    print("%.2f %f" % (k, ror))
    #time.sleep(0.2)