import time
import pyupbit as ub
import datetime
import requests
import pandas as pd


tickers = ub.get_tickers(fiat='KRW') #원화 마켓 코인 목록 받아오기

print(tickers)

volumes = []
for ticker in tickers:
    df = ub.get_ohlcv(ticker, interval="hour", count=24)
    volumes.insert(-1,round(df.iloc[-1]["value"])) #거래대금 목록에 추가
    print(df)
    print(ticker)
    print(round(df.iloc[-1]["value"]))

    time.sleep(0.1)