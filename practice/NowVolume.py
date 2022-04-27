import time
import pyupbit as ub
import datetime
import requests
import pandas as pd


access = "RLiPx3Sw77GaJmGJF0jiEx5ex3C2tk3BoRZoKELC"
secret = "jbDUQl89zUoUxVWqlFdn6ziWTwpcoBTz1sBpJGva"

tickers = ub.get_tickers(fiat='KRW')
volumes = []
for ticker in tickers:
    df = ub.get_ohlcv(ticker, interval="hour", count=24)
    volumes.insert(-1,round(df.iloc[-1]["volume"]*df.iloc[0]['close']))
    print(ticker)
    print(round(df.iloc[-1]["volume"]*df.iloc[0]['close']))

    time.sleep(0.1)
    #print("working...")

print(volumes)
#tmp = max(volumes)
#biggest = volumes.index(tmp)
print(tickers)
#print(biggest)
#print(tickers[biggest])
